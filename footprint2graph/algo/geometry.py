# -*- coding: utf-8 -*-

import math
import progressbar
# from rtree import index
import tracklib as tkl

from scipy.spatial import cKDTree
import numpy as np


"""
Fonctions qui manipulent les géométries (de type ligne) des arcs 
sans gérer la topologie (en particulier les noeuds).
"""


def snap_lines_to_connect(collection, tolerance=1, log_level='ERROR'):
    """
    Snap lines representing network arcs to connect them within a given tolerance.

    This operation handles the splitting of lines when snapping occurs 
               away from their endpoints. However, it does not handle 
               the small line segments created by this splitting operation.

    Parameters
    ----------
    collection : TrackCollection
        Collection of line geometries representing network arcs.
    tolerance : float, optional
        Maximum distance within which line geometries are snapped together,
        in the units of the coordinate reference system. Default is 1.
    log_level : str, optional
        Logging level used during the operation. Default is 'ERROR'.

    Returns
    -------
    TrackCollection
        A new collection containing the snapped line geometries.

    """

    # On indexe la collection pour rechercher uniquement les traces candidates
    #    qui par définition sont proches.
    print ('')
    index = tkl.SpatialIndex(collection)
    unit = max(math.ceil(tolerance/index.dX), math.ceil(tolerance/index.dY))

    if log_level == 'INFO' or log_level == 'DEBUG':
        print ('')
        print ('    Start snapping')
    if log_level == 'DEBUG':
        print ('        Unit for search in index ', unit)

    CUTS = {}

    # for track1 in collection:
    boucle = progressbar.progressbar(range(collection.size()))
    for i in boucle:
        track1 = collection.getTrack(i)

        # for track2 in collection:
        voisins = index.neighborhood(track1, unit=unit)
        for j in voisins:
            track2 = collection.getTrack(j)

            if track1.tid == track2.tid:
                if log_level == 'DEBUG':
                    print("        track1 and track2 are the same tracks")
                continue

            if not tkl.intersects(track1, track2):

                # Vérifier la distance
                dist = line_distance(track1, track2)
                if dist < tolerance and dist > 0.0:

                    if log_level == 'DEBUG':
                        print("        Snap needed", track1.tid, track2.tid, round(dist, 2))

                    # Trouver les points les plus proches pour les 2 traces
                    idxi, idxj = nearest_points(track1, track2)
                    p2 = track2.getObs(idxj).position

                    # On remplace dans la première trace
                    #        le point le plus proche pour qu'il soit dans trace 2
                    track1.setObs(idxi, tkl.Obs(p2, tkl.ObsTime()))

                    # On coupe la trace 1 si besoin
                    if idxi > 0 and idxi < track1.size()-1:
                        if log_level == 'DEBUG':
                            print ('        on coupe la trace 1')

                        if i not in CUTS:
                            CUTS[i] = []
                        CUTS[i].append((idxi,p2))

                    # On coupe la trace 2 si besoin
                    if idxj > 0 and idxj < track2.size()-1:
                        if log_level == 'DEBUG':
                            print ('    on coupe la trace 2')

                        if j not in CUTS:
                            CUTS[j] = []
                        CUTS[j].append((idxj,p2))

    # On coupe les traces

    # Compteur pour les nouvelles traces
    cptTrack = collection.size() + 1

    TRACK_TO_REMOVE = []
    for idtrack in CUTS:
        obss = CUTS[idtrack]
        res = sorted(obss, key=lambda t: t[0])
        #print (idtrack)
        #if len(obss) > 1:
        #    print (collection.getTrack(idtrack).toWKT())

        track = collection.getTrack(idtrack)

        for i in range(len(res)):
            idx = res[i][0]

            if i == len(res)-1:
                end = track.size()-1
            else:
                end = res[i+1][0]

            # print (0, idx, end, track.size())

            # on en crée 2 nouveaux
            s1 = track.extract(0, idx)
            s1.tid = cptTrack
            cptTrack += 1
            collection.addTrack(s1)


            s2 = track.extract(idx, end)
            s2.tid = cptTrack
            cptTrack += 1
            collection.addTrack(s2)

        # on supprime la track
        TRACK_TO_REMOVE.append(track)

    for track in TRACK_TO_REMOVE:
        collection.removeTrack(track)

    return collection




def segment_distance(a1, a2, b1, b2):
    return min (
        tkl.distance_to_segment(a1.getX(), a1.getY(), b1.getX(), b1.getY(), b2.getX(), b2.getY()),
        tkl.distance_to_segment(a2.getX(), a2.getY(), b1.getX(), b1.getY(), b2.getX(), b2.getY()),
        tkl.distance_to_segment(b1.getX(), b1.getY(), a1.getX(), a1.getY(), a2.getX(), a2.getY()),
        tkl.distance_to_segment(b2.getX(), b2.getY(), a1.getX(), a1.getY(), a2.getX(), a2.getY()),
    )



def line_distance(track1, track2):
    '''
    Distance entre 2 traces: distance minimum entre 2 sommets

    Parameters
    ----------
    track1 : TYPE
        DESCRIPTION.
    track2 : TYPE
        DESCRIPTION.

    Returns
    -------
    min_dist : TYPE
        DESCRIPTION.

    '''
    min_dist = float('inf')

    for i in range(track1.size() - 1):
        p1i = track1.getObs(i).position
        p1i1 = track1.getObs(i+1).position
        for j in range(track2.size() - 1):
            p2j = track2.getObs(j).position
            p2j1 = track2.getObs(j+1).position
            d = segment_distance (p1i, p1i1, p2j, p2j1)
            min_dist = min(min_dist, d)

    return min_dist


def nearest_points(track1, track2):
    maxd = float('inf')
    idxi = -1
    idxj = -1
    for i in range(track1.size()):
        o1 = track1.getObs(i)
        for j in range(track2.size()):
            o2 = track2.getObs(j)
            d = o1.position.distance2DTo(o2.position)
            if d < maxd:
                idxi = i
                idxj = j
                maxd = d
    return (idxi, idxj)


def distance_point_track(o, track):
    pos = 0
    d = o.distanceTo(track.getFirstObs())

    for i in range(1, track.size()):
        if o.distanceTo(track.getObs(i)) < d:
            pos = i
            d = o.distanceTo(track.getObs(i))
    return (d, pos)


def decoupe_trace(track, I):
    '''
    Pas de topologie, uniquement la géométrie qu'on découpe
    '''

    # Trouver le point de la trace le plus proche
    dmin1 = float('inf')
    i1 = -1
    for i in range(len(track)):
        oi = track.getObs(i)
        d = oi.position.distance2DTo(I.position)
        if d < dmin1:
            dmin1 = d
            i1 = i

    # On remplace dans la trace le point d'intersection
    track.setObs(i1, tkl.Obs(I.position.copy(), tkl.ObsTime()))

    s1 = None
    s2 = None

    # On coupe la trace à ce nouveau point d'intersection
    if i1 > 0 and i1 < track.size()-1:
        # on crée 2 nouvelles traces
        s1 = track.extract(0, i1)
        s2 = track.extract(i1, track.size()-1)
    elif i1 == 0:
        s1 = None
        s2 = track
    elif i1 == track.size()-1:
        s1 = track
        s2 = None

    return (s1, s2)



def extend_extremity(track, length=50, pos='END', verbose=True):
    '''
    Extend start point or end point 

    Parameters
    ----------
    track : TYPE
        DESCRIPTION.
    length : TYPE, optional
        DESCRIPTION. The default is 50.
    pos : {'START', 'END'}, optional
        DESCRIPTION. The default is 'END'.

    Returns
    -------
    track : TYPE
        DESCRIPTION.

    '''

    track.removePosDup()
    if track.size() < 2:
        if verbose:
            print ("        Track contains too few points (" + str(track.size()) + ")")
        return None

    if pos == 'END':
        p1 = track[-2]
        p2 = track[-1]
    else:
        p1 = track[1]
        p2 = track[0]

    if p1.position == p2.position:
        if verbose:
            print ("        Track contains same points.")
        return None

    dx = p2.position.getX() - p1.position.getX()
    dy = p2.position.getY() - p1.position.getY()

    norm = math.hypot(dx, dy)

    dx /= norm
    dy /= norm

    p3 = (
        p2.position.getX() + length * dx,
        p2.position.getY() + length * dy
    )

    track = tkl.Track()
    c2 = tkl.ENUCoords(p2.position.getX(), p2.position.getY())
    track.addObs(tkl.Obs(c2, tkl.ObsTime()))
    c3 = tkl.ENUCoords(p3[0], p3[1])
    track.addObs(tkl.Obs(c3, tkl.ObsTime()))

    return track


def get_final_edges(edge_id, splits):
    '''
    Récupére les arcs terminaux de edge_id dans l'arbre de découpage SPLITS

    Parameters
    ----------
    edge_id : TYPE
        DESCRIPTION.
    splits : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''

    if edge_id not in splits:
        return [edge_id]

    result = []

    for child in splits[edge_id]:
        result.extend(get_final_edges(child, splits))

    return result



def find_connection_candidate(network, edge, extension, side):
    '''
    Searches for the closest network edge that intersects an extension of a given edge.
    '''


    if side == "START":
        ref_pos = edge.geom.getFirstObs().position
    else:
        ref_pos = edge.geom.getLastObs().position

    point_inters = None
    edge_to_split = None
    min_dist = float("inf")

    neighbor_idxs1 = network.spatial_index.neighborhood(edge.geom, unit=-1)
    neighbor_idxs2 = network.spatial_index.neighborhood(extension, unit=-1)
    neighbor_idxs = set(neighbor_idxs1) | set(neighbor_idxs2)

    for idx in neighbor_idxs:
        neighbor = network[idx]
        if neighbor.id == edge.id:
            continue

        intersections = tkl.intersection(extension, neighbor.geom, withTime=-1)
        for intersec in intersections:

            dist = intersec.position.distance2DTo(ref_pos)

            if dist < min_dist:
                min_dist = dist
                point_inters = intersec
                edge_to_split = neighbor

    if edge_to_split is None:
        return None

    return {
        "edge": edge.id,
        "side": side,
        "intersection": point_inters,
        "edge_to_split": edge_to_split.id,
        "extension": extension,
        "dist": min_dist
    }




def pull_point_to_other_tracks(cutCollection, buffer_size=10, alpha=0.6):
    """
    Move trajectory points closer to neighboring trajectories to make
    spatially close trajectories more tightly clustered.

    For each trajectory point, neighboring trajectory points within a given
    buffer are identified. The point is then moved towards the centroid of
    these neighboring points. The displacement is controlled by `alpha`.

    This operation is intended to bring trajectories closer together between
    two successive iterations of the workflow, in order to assess whether
    this improves the detection of spatial patterns in the resulting network.

    Parameters
    ----------
    cutCollection : TrackCollection
        Collection of trajectories to be processed.
    buffer_size : float, optional
        Size of the buffer used to identify neighboring trajectory points,
        in the units of the coordinate reference system. Default is 10.
    alpha : float, optional
        Weight controlling the displacement of each point towards the
        centroid of neighboring points. A value of 0 leaves the point
        unchanged, while a value of 1 moves it to the centroid.
        Default is 0.6.

    Returns
    -------
    TrackCollection
        A new collection containing the trajectories with their points moved
        towards neighboring trajectories.
    """

    print ('        Attract points toward the centroid of neighboring trajectory points')

    # Create a 2D index
    #p = index.Property()
    #p.dimension = 2
    #idx2d = index.Index(properties=p)

    print ("        Create index and index all observations not map-matched")
    num = 1
    boucle = progressbar.progressbar(range(cutCollection.size()))

    points = []
    coords = {}

    for i in boucle:
        track = cutCollection.getTrack(i)
        for j in range(track.size()):
            o = track.getObs(j)
            x = o.position.getX()
            y = o.position.getY()

            coords[len(points)] = (i, j)
            points.append((x, y))

    points = np.asarray(points)
    tree = cKDTree(points)

    '''
    for i in boucle:
        track = cutCollection.getTrack(i)
        for j in range(track.size()):
            o = track.getObs(j)
            x = o.position.getX()
            y = o.position.getY()
            idx2d.insert(
                num,
                (x, y, x, y),
                obj=(i, j)
            )
            num += 1
    '''

    print ('\n        Pull points toward the centroid of neighboring trajectory points')
    boucle = progressbar.progressbar(range(cutCollection.size()))

    for i in boucle:
        track = cutCollection.getTrack(i)
        for j in range(track.size()):
            o = track.getObs(j)

            cluster = tkl.Track()
    
            x, y = o.position.getX(), o.position.getY()
            idxs = tree.query_ball_point([x, y], r=(buffer_size+1))

            for idx in idxs:
                ia, ja = coords[idx]
                if ia == i:
                    continue
                voisin = cutCollection[ia].getObs(ja)
                if voisin.distance2DTo(o) <= buffer_size:
                    cluster.addObs(voisin)

            if cluster.size() > 0:
                centre = cluster.getCentroid()
                x_new = o.position.getX() + alpha * (centre.getX() - o.position.getX())
                y_new = o.position.getY() + alpha * (centre.getY() - o.position.getY())
                o.position = tkl.ENUCoords(x_new, y_new)


    '''
    for i in boucle:
        track = cutCollection.getTrack(i)
        for j in range(track.size()):
            o = track.getObs(j)

            cluster = tkl.Track()
    
            x, y = o.position.getX(), o.position.getY()
            # 1m de marge au cas où
            bbox = (x - buffer_size-1, y - buffer_size-1,
                    x + buffer_size+1, y + buffer_size+1)
    
            # Identifiants candidats
            candidates = idx2d.intersection(bbox, objects=True)
            for item in candidates:
                (ia, ja) = item.object
                if ia == i:
                    continue
                voisin = cutCollection[ia].getObs(ja)
                if voisin.distance2DTo(o) <= buffer_size:
                    cluster.addObs(voisin)

            if cluster.size() > 0:
                centre = cluster.getCentroid()
                x_new = o.position.getX() + alpha * (centre.getX() - o.position.getX())
                y_new = o.position.getY() + alpha * (centre.getY() - o.position.getY())
                o.position = tkl.ENUCoords(x_new, y_new)
    '''


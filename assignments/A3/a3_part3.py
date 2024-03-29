"""CSC111 Winter 2022 Assignment 3: Graphs, Recommender Systems, and Clustering (Part 3)

Instructions (READ THIS FIRST!)
===============================

This Python module contains the functions you'll write for determining *clusters* of vertices
in a graph.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2022 Mario Badr, David Liu, and Isaac Waller.
"""
import random
from typing import Literal

from a3_part2_recommendations import WeightedGraph


################################################################################
# Part 3, Q1
################################################################################
def create_book_graph(review_graph: WeightedGraph,
                      threshold: float = 0.05,
                      score_type: Literal['unweighted', 'strict'] = 'unweighted') -> WeightedGraph:
    """Return a book graph based on the given review_graph.

    The score_type parameter plays the same role as in WeightedGraph.get_similarity_score.

    The returned book graph has the following properties:
        1. Its vertex set is exactly the set of book vertices in review_graph
            (items are book titles).
        2. For every two distinct books b1 and b2, let s(b1, b2) be their similarity score,
            where score_type specifies which similarity score to use.

            - If s(b1, b2) > threshold, there is an edge between b1 and b2 in the book graph
              with weight equal to s(b1, b2). Unlike Part 2, these weights will be floats,
              not ints!
            - Otherwise, there is no edge between b1 and b2.

    Preconditions:
        - score_type in {'unweighted', 'strict'}
    """
    # Add all books as vertices
    book_graph = WeightedGraph()
    book_names: set[str] = review_graph.get_all_vertices('book')
    for b in book_names:
        book_graph.add_vertex(b, 'book')

    # Add all edges
    for b1 in book_names:
        for b2 in book_names:
            if b1 == b2:
                continue

            # Calculate similarity score
            score = review_graph.get_similarity_score(b1, b2, score_type)
            if score <= threshold:
                continue

            # Add edge
            book_graph.add_edge(b1, b2, score)

    # Done
    return book_graph


################################################################################
# Part 3, Q2
################################################################################
def cross_cluster_weight(book_graph: WeightedGraph, cluster1: set, cluster2: set) -> float:
    """Return the cross-cluster weight between cluster1 and cluster2.

    See assignment handout for the definition of cross-cluster weight.

    Preconditions:
        - cluster1 != set() and cluster2 != set()
        - cluster1.isdisjoint(cluster2)
        - Every item in cluster1 and cluster2 is a vertex in book_graph

    >>> bg = WeightedGraph()
    >>> for b in range(4): \
            bg.add_vertex(f'B{b}', 'book')
    >>> bg.add_edge('B0', 'B1', .5)
    >>> bg.add_edge('B0', 'B2', .4)
    >>> bg.add_edge('B1', 'B2', .3)
    >>> bg.get_weight('B0', 'B1')
    0.5
    >>> cross_cluster_weight(bg, {'B0', 'B1'}, {'B2', 'B3'}) == (.4 + .3) / 4
    True
    """
    # sw = sum(book_graph.get_weight(v1, v2) for v1 in cluster1 for v2 in cluster2)
    sw = 0
    for v1 in cluster1:
        for v2 in cluster2:
            sw += book_graph.get_weight(v1, v2)

    return sw / (len(cluster1) * len(cluster2))


################################################################################
# Part 3, Q3 (don't modify this code)
################################################################################
def find_clusters_random(graph: WeightedGraph, num_clusters: int) -> list[set]:
    """Return a list of <num_clusters> vertex clusters for the given graph.

    At each iteration, this algorithm first chooses a random cluster, and then chooses
    the cluster that has the highest cross-cluster weight to the randomly-chose cluster
    to merge.

    Preconditions:
        - num_clusters >= 1
    """
    # Each book starts in its own cluster
    clusters = [{book} for book in graph.get_all_vertices()]

    for _ in range(0, len(clusters) - num_clusters):
        print(f'{len(clusters)} clusters')

        c1 = random.choice(clusters)
        # Pick the best cluster to merge c1 into.
        best = -1
        best_c2 = None

        for c2 in clusters:
            if c1 is not c2:
                score = cross_cluster_weight(graph, c1, c2)
                if score > best:
                    best = score
                    best_c2 = c2

        best_c2.update(c1)
        clusters.remove(c1)

    return clusters


def find_clusters_greedy(graph: WeightedGraph, num_clusters: int) -> list[set]:
    """Return a list of <num_clusters> vertex clusters for the given graph.

    At each iteration, this algorithm chooses the pair of clusters with the highest
    cross-cluster weight to merge.

    Preconditions:
        - num_clusters >= 1
    """
    # Each book starts in its own cluster
    clusters = [{book} for book in graph.get_all_vertices()]

    for _ in range(0, len(clusters) - num_clusters):
        print(f'{len(clusters)} clusters')

        # Merge the two communities with the most links
        best = -1
        best_c1, best_c2 = None, None

        for i1 in range(0, len(clusters)):
            for i2 in range(i1 + 1, len(clusters)):
                c1, c2 = clusters[i1], clusters[i2]
                score = cross_cluster_weight(graph, c1, c2)
                if score > best:
                    best, best_c1, best_c2 = score, c1, c2

        best_c2.update(best_c1)
        clusters.remove(best_c1)

    return clusters


if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # increases the running time of the functions/methods.
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 1000,
        'disable': ['E1136'],
        'extra-imports': ['random', 'a3_part2_recommendations'],
        'allowed-io': ['find_clusters_greedy', 'find_clusters_random'],
        'max-nested-blocks': 4
    })

    # Q1 Test
    # review_graph = load_weighted_review_graph('data/reviews_full.csv', 'data/book_names.csv')
    # book_graph = create_book_graph(review_graph, 0.03)
    # from a3_visualization import visualize_graph
    # visualize_graph(book_graph)

    # Q3 Test
    # review_graph = load_weighted_review_graph('data/reviews_full.csv', 'data/book_names.csv')
    # book_graph = create_book_graph(review_graph, threshold=0.01, score_type='strict')
    # clusters = find_clusters_random(book_graph, 15)
    # from a3_visualization import visualize_graph_clusters
    # visualize_graph_clusters(book_graph, clusters)

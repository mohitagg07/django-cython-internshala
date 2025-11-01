# shop/recommender_cy.pyx

cdef float c_calculate_similarity(set tags1, set tags2):
    """
    A Cython-native (cdef) function for speed.
    """
    cdef int intersection_len = len(tags1.intersection(tags2))
    cdef int union_len = len(tags1.union(tags2))

    if union_len == 0:
        return 0.0
        
    return <float>intersection_len / union_len

# This is the "def" function that Python (our Django app) can call
# --- THIS FUNCTION SIGNATURE HAS CHANGED ---
def get_recommendations_cy(current_product_tags, all_products_data, set liked_ids, set disliked_ids):
    """
    The Cython-optimized HYBRID recommender.
    'all_products_data' is a list of tuples: [(id, ['tag1', 'tag2']), ...]
    'liked_ids' is a set of product IDs the user has liked.
    'disliked_ids' is a set of product IDs the user has disliked.
    """
    
    cdef list recommendations = []
    cdef set current_tags_set = set(current_product_tags)
    cdef float score
    
    cdef int product_id
    cdef list product_tags
    cdef set product_tags_set

    for product_id, product_tags in all_products_data:
        
        # --- NEW AI LOGIC (PART 1) ---
        # If user disliked this item, skip it entirely
        if product_id in disliked_ids:
            continue
            
        product_tags_set = set(product_tags)
        
        # Use the C-native function
        score = c_calculate_similarity(current_tags_set, product_tags_set)
        
        # --- NEW AI LOGIC (PART 2) ---
        # If user liked this item, give it a significant score boost
        if product_id in liked_ids:
            score += 0.5  # This boost makes it a hybrid model!
        
        if score > 0.1:
            recommendations.append((score, product_id))
            
    recommendations.sort(key=lambda x: x[0], reverse=True)
    
    return [product_id for score, product_id in recommendations[:3]]
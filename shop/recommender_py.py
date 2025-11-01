# shop/recommender_py.py

def calculate_similarity(tags1, tags2):
    """
    Calculates a simple similarity score based on common tags.
    """
    set1 = set(tags1)
    set2 = set(tags2)
    
    # Simple Jaccard Index (intersection over union)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    if union == 0:
        return 0.0
        
    return intersection / union

def get_recommendations_py(current_product, all_products):
    """
    The "pure Python" recommendation function.
    This is the function we will optimize.
    """
    current_tags = current_product.get_tags_list()
    recommendations = []

    # This loop is the "computation-heavy" part
    for product in all_products:
        if product.id == current_product.id:
            continue
            
        other_tags = product.get_tags_list()
        score = calculate_similarity(current_tags, other_tags)
        
        if score > 0.1: # Only recommend if score is somewhat decent
            recommendations.append((score, product))
            
    # Sort by score, descending
    recommendations.sort(key=lambda x: x[0], reverse=True)
    
    # Return just the top 3 products
    return [product for score, product in recommendations[:3]]
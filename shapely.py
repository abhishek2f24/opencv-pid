from shapely.geometry import Point, Polygon

# Define the rectangle coordinates of the word
rectangle = Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

# List of other tag/word rectangles
other_rectangles = [
    Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)]),
    Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)]),
    # Add more rectangles as needed
]

# Calculate the nearest tag/word
nearest_distance = float('inf')
nearest_tag = None

for other_rectangle in other_rectangles:
    distance = rectangle.distance(other_rectangle)
    if distance < nearest_distance:
        nearest_distance = distance
        nearest_tag = other_rectangle.tag  # Replace with the actual attribute of the tag/word

print("Nearest Tag:", nearest_tag)
print("Distance:", nearest_distance)

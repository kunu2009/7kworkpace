"""
Workspace Organizer - Icon Generator
Creates a simple icon for the application
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a simple icon for the application"""
    # Create a new image with gradient-like appearance
    size = 256
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)
    
    # Background - gradient effect (simulated with rectangles)
    for i in range(size):
        # Create gradient from #667eea to #764ba2
        r = int(102 + (118 - 102) * (i / size))
        g = int(126 + (75 - 126) * (i / size))
        b = int(234 + (162 - 234) * (i / size))
        draw.line([(0, i), (size, i)], fill=(r, g, b))
    
    # Draw calendar-like appearance
    # Top section - date
    draw.rectangle([20, 20, 120, 80], outline='white', width=3)
    draw.text((50, 40), "WO", fill='white', font=None)
    
    # Grid for files
    grid_start = 100
    cell_size = 30
    for row in range(2):
        for col in range(3):
            x = grid_start + col * cell_size
            y = grid_start + row * cell_size
            draw.rectangle([x, y, x + cell_size - 2, y + cell_size - 2], 
                          outline='white', width=2)
    
    # Save as ICO
    img.save('icon.ico', format='ICO', sizes=[(256, 256)])
    print("✅ Icon created successfully: icon.ico")

if __name__ == "__main__":
    create_icon()

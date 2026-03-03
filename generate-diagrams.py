#!/usr/bin/env python3
"""
Generate architecture diagrams for blog posts
Uses matplotlib to create clean, Excalidraw-style diagrams
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np
import os

diagrams_dir = "/home/opc/.openclaw/workspace/autonomous-researcher/assets/diagrams"

def draw_box(ax, x, y, width, height, text, color="#e3f2fd", text_color="#1565c0"):
    """Draw a rounded box similar to Excalidraw style"""
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                         boxstyle="round,pad=0.02,rounding_size=0.15",
                         facecolor=color, edgecolor=text_color, linewidth=2)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=10, 
            color=text_color, fontweight='bold', wrap=True)
    return box

def draw_arrow(ax, start, end, color="#666666"):
    """Draw an arrow between two points"""
    arrow = FancyArrowPatch(start, end, 
                           arrowstyle='->', mutation_scale=20, 
                           color=color, linewidth=2)
    ax.add_patch(arrow)

def draw_user(ax, x, y):
    """Draw a user icon"""
    circle = Circle((x, y + 0.15), 0.1, facecolor='#fff9c4', edgecolor='#f9a825', linewidth=2)
    ax.add_patch(circle)
    body = FancyBboxPatch((x - 0.12, y - 0.25), 0.24, 0.25,
                         boxstyle="round,pad=0.02", 
                         facecolor='#fff9c4', edgecolor='#f9a825', linewidth=2)
    ax.add_patch(body)
    ax.text(x, y - 0.4, "User", ha='center', fontsize=9, color='#f9a825', fontweight='bold')

def draw_cloud(ax, x, y, label, color="#e8f5e9"):
    """Draw a cloud shape"""
    # Simplified cloud as rounded box
    box = FancyBboxPatch((x - 0.5, y - 0.2), 1.0, 0.4,
                         boxstyle="round,pad=0.02,rounding_size=0.2",
                         facecolor=color, edgecolor="#2e7d32", linewidth=2)
    ax.add_patch(box)
    ax.text(x, y, label, ha='center', va='center', fontsize=10,
            color='#2e7d32', fontweight='bold')

def generate_alb_diagram():
    """Generate ALB architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Title
    ax.text(5, 5.5, "Application Load Balancer Architecture", 
            ha='center', fontsize=14, fontweight='bold', color='#333')
    
    # Users
    draw_user(ax, 1, 4)
    draw_user(ax, 1, 2.5)
    
    # ALB
    draw_box(ax, 4, 3.5, 2, 1, "ALB\n(Layer 7)", "#bbdefb", "#1565c0")
    
    # Target Groups
    draw_box(ax, 7.5, 5, 1.8, 0.8, "/api/*\nAPI Servers", "#c8e6c9", "#2e7d32")
    draw_box(ax, 7.5, 3.5, 1.8, 0.8, "/web/*\nWeb Servers", "#c8e6c9", "#2e7d32")
    draw_box(ax, 7.5, 2, 1.8, 0.8, "/static\nS3 Bucket", "#ffccbc", "#d84315")
    
    # Arrows from users to ALB
    draw_arrow(ax, (1.3, 4), (3, 3.8))
    draw_arrow(ax, (1.3, 2.5), (3, 3.2))
    
    # Arrows from ALB to targets
    draw_arrow(ax, (5, 4.2), (6.6, 4.8))
    draw_arrow(ax, (5, 3.5), (6.6, 3.5))
    draw_arrow(ax, (5, 2.8), (6.6, 2.2))
    
    # Labels
    ax.text(2.2, 4.3, "HTTPS", fontsize=8, color='#666')
    ax.text(5.8, 4.8, "Route", fontsize=8, color='#666')
    ax.text(5.8, 3.5, "Route", fontsize=8, color='#666')
    ax.text(5.8, 2.5, "Route", fontsize=8, color='#666')
    
    plt.tight_layout()
    plt.savefig(f"{diagrams_dir}/alb-architecture.png", dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"Generated: {diagrams_dir}/alb-architecture.png")

def generate_nlb_diagram():
    """Generate NLB architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Title
    ax.text(5, 5.5, "Network Load Balancer Architecture", 
            ha='center', fontsize=14, fontweight='bold', color='#333')
    
    # Users
    draw_user(ax, 1, 3.5)
    
    # Static IP label
    ax.text(3.5, 4.8, "Static IP per AZ", fontsize=9, color='#666', style='italic')
    
    # NLB
    draw_box(ax, 4, 3.5, 2, 1, "NLB\n(Layer 4)\nTCP/UDP", "#fff3e0", "#e65100")
    
    # Targets
    draw_box(ax, 7.5, 4.5, 1.8, 0.7, "TCP 443\nWeb Servers", "#e1f5fe", "#0277bd")
    draw_box(ax, 7.5, 3.5, 1.8, 0.7, "TCP 3306\nDatabases", "#f3e5f5", "#7b1fa2")
    draw_box(ax, 7.5, 2.5, 1.8, 0.7, "UDP 53\nDNS Servers", "#e8f5e9", "#388e3c")
    
    # Arrows
    draw_arrow(ax, (1.3, 3.5), (3, 3.5), "#e65100")
    draw_arrow(ax, (5, 4), (6.6, 4.5))
    draw_arrow(ax, (5, 3.5), (6.6, 3.5))
    draw_arrow(ax, (5, 3), (6.6, 2.8))
    
    # Features
    ax.text(4, 1.5, "✓ Millions of TPS  ✓ Ultra-low latency (~100μs)  ✓ Static IP  ✓ Preserve client IP",
            ha='center', fontsize=9, color='#555', 
            bbox=dict(boxstyle='round', facecolor='#f5f5f5', edgecolor='#ddd'))
    
    plt.tight_layout()
    plt.savefig(f"{diagrams_dir}/nlb-architecture.png", dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"Generated: {diagrams_dir}/nlb-architecture.png")

def generate_cloudfront_diagram():
    """Generate CloudFront CDN diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    
    # Title
    ax.text(6, 6.5, "CloudFront CDN Architecture", 
            ha='center', fontsize=14, fontweight='bold', color='#333')
    
    # Users worldwide
    draw_user(ax, 1, 5.5)
    ax.text(1, 4.8, "User in\nNYC", ha='center', fontsize=8)
    
    draw_user(ax, 1, 2.5)
    ax.text(1, 1.8, "User in\nLondon", ha='center', fontsize=8)
    
    # Edge locations
    draw_cloud(ax, 4.5, 5.5, "Edge Location\nNYC", "#e3f2fd")
    draw_cloud(ax, 4.5, 2.5, "Edge Location\nLondon", "#e3f2fd")
    
    # Origin
    draw_box(ax, 9, 4, 2.5, 1.5, "Origin Server\n(S3 / ALB / EC2)", "#ffebee", "#c62828")
    
    # Arrows user to edge
    draw_arrow(ax, (1.4, 5.5), (4, 5.5))
    draw_arrow(ax, (1.4, 2.5), (4, 2.5))
    
    # Cache hit/miss
    ax.text(4.5, 4.8, "Cache HIT", fontsize=8, color='#2e7d32', fontweight='bold')
    ax.text(4.5, 1.8, "Cache MISS", fontsize=8, color='#d84315', fontweight='bold')
    
    # Arrow from edge to origin
    draw_arrow(ax, (5, 2.8), (8, 3.5))
    
    # Return arrows
    draw_arrow(ax, (4.5, 5), (1.4, 5))
    draw_arrow(ax, (8, 4), (5, 2.2))
    draw_arrow(ax, (4.5, 2), (1.4, 2.2))
    
    # Stats
    ax.text(6, 0.8, "450+ Edge Locations Worldwide  |  Sub-100ms Latency  |  DDoS Protection",
            ha='center', fontsize=9, color='#555',
            bbox=dict(boxstyle='round', facecolor='#f5f5f5', edgecolor='#ddd'))
    
    plt.tight_layout()
    plt.savefig(f"{diagrams_dir}/cloudfront-architecture.png", dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"Generated: {diagrams_dir}/cloudfront-architecture.png")

if __name__ == '__main__':
    os.makedirs(diagrams_dir, exist_ok=True)
    generate_alb_diagram()
    generate_nlb_diagram()
    generate_cloudfront_diagram()
    print("\nAll diagrams generated successfully!")

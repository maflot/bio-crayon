#!/usr/bin/env python3
"""
Minimal colormap example demonstrating metadata requirements.
"""

import sys
import os

sys.path.append(".")

from bio_crayon import BioCrayon


def demonstrate_metadata_requirements():
    """Demonstrate the difference between user and community colormap metadata requirements."""

    print("🎨 BioCrayon Metadata Requirements Demo")
    print("=" * 50)

    # Example 1: User colormap (metadata optional)
    print("\n1️⃣ User Colormap (Metadata Optional)")
    print("-" * 40)

    user_colormap = {
        "colormaps": {
            "my_custom_colors": {
                "type": "categorical",
                "colors": {"red": "#FF0000", "green": "#00FF00", "blue": "#0000FF"},
            }
        }
    }

    try:
        bc_user = BioCrayon(user_colormap)
        print("✅ User colormap loaded successfully (no metadata required)")
        print(f"Available colormaps: {bc_user.list_colormaps()}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Example 2: User colormap with metadata (still valid)
    print("\n2️⃣ User Colormap with Metadata (Optional)")
    print("-" * 40)

    user_colormap_with_metadata = {
        "metadata": {
            "name": "My Custom Colormaps",
            "version": "1.0",
            "description": "Personal colormap collection",
        },
        "colormaps": {
            "my_custom_colors": {
                "type": "categorical",
                "colors": {"red": "#FF0000", "green": "#00FF00", "blue": "#0000FF"},
            }
        },
    }

    try:
        bc_user_with_meta = BioCrayon(user_colormap_with_metadata)
        print("✅ User colormap with metadata loaded successfully")
        metadata = bc_user_with_meta.get_metadata()
        print(f"Metadata: {metadata}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Example 3: Community colormap (metadata required)
    print("\n3️⃣ Community Colormap (Metadata Required)")
    print("-" * 40)

    community_colormap = {
        "metadata": {
            "name": "Community Brain Atlas",
            "version": "1.0",
            "description": "Colormaps for brain region visualization",
            "author": "Neuroscience Lab",
            "doi": "10.1000/example.doi",
            "keywords": ["brain", "atlas", "neuroscience"],
        },
        "colormaps": {
            "brain_regions": {
                "type": "categorical",
                "colors": {
                    "cortex": "#FF6B6B",
                    "hippocampus": "#4ECDC4",
                    "cerebellum": "#45B7D1",
                },
            }
        },
    }

    try:
        # This would be loaded via from_community() which enforces metadata
        bc_community = BioCrayon(community_colormap, require_metadata=True)
        print("✅ Community colormap loaded successfully (metadata validated)")
        metadata = bc_community.get_metadata()
        print(f"Metadata: {metadata}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Example 4: Invalid community colormap (missing metadata)
    print("\n4️⃣ Invalid Community Colormap (Missing Metadata)")
    print("-" * 40)

    invalid_community_colormap = {
        "colormaps": {
            "brain_regions": {
                "type": "categorical",
                "colors": {"cortex": "#FF6B6B", "hippocampus": "#4ECDC4"},
            }
        }
    }

    try:
        # This should fail because metadata is required for community colormaps
        bc_invalid = BioCrayon(invalid_community_colormap, require_metadata=True)
        print("❌ Should have failed - missing metadata")
    except Exception as e:
        print(f"✅ Correctly rejected: {e}")

    print("\n" + "=" * 50)
    print("📋 Summary:")
    print("• User colormaps: Metadata is optional")
    print("• Community colormaps: Metadata with 'name' and 'version' is required")
    print("• Both types must have valid colormap structure")
    print("• Community colormaps are validated more strictly")


if __name__ == "__main__":
    demonstrate_metadata_requirements()

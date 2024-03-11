"""
Resources object for the pygame renderer

This object should have lots of misc methods for rendering any other
parts of the interactive pygame renderer, including:
    - Velocity direction display (with magnitude)
    - Mesh dimensions clearly labeled
    - FPS and performance details
    - "ESC to exit" text
    - Title

Should work on the principle of dependency injection, where it is
agnostic to the particular pygame "surface" object it is sent.
"""

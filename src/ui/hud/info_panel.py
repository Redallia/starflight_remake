"""
Base info panel for upper-right contextual information
Upper-right of screen, 300x200
"""
from ui.hud.hud_panel import HUDPanel


class InfoPanel(HUDPanel):
    """
    Base class for contextual info panels in upper-right

    Different screens can swap in different info panels:
    - SpaceScreen uses MiniMapPanel
    - HyperspaceScreen could use ShipInfoPanel
    - CommunicationScreen could use AlienInfoPanel
    """

    def __init__(self, x, y, width, height):
        """
        Initialize info panel

        Args:
            x: X position on screen
            y: Y position on screen
            width: Panel width (300)
            height: Panel height (200)
        """
        super().__init__(x, y, width, height)

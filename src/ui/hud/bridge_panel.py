"""
Bridge panel for displaying ship crew positions
Shows: Captain, Navigator, Engineer, Science, Communications, Medic
Can also display role-specific menus
Uses GenericMenuPanel for rendering
"""
from ui.hud.generic_menu_panel import GenericMenuPanel, MenuConfig


class BridgePanel(GenericMenuPanel):
    """Bridge display panel - shows crew role stations"""

    def __init__(self, x, y, width, height):
        """
        Initialize bridge panel

        Args:
            x: X position on screen
            y: Y position on screen
            width: Panel width
            height: Panel height
        """
        # Define the six crew roles
        self.roles = [
            "Captain",
            "Science Officer",
            "Navigator",
            "Engineer",
            "Communications",
            "Doctor"
        ]

        # Initialize with bridge config
        config = MenuConfig(
            title="Bridge",
            items=self.roles
        )
        super().__init__(x, y, width, height, config)

        # Role menu state
        self.active_role = None  # Which role's menu is active (None = showing role list)
        self.role_menus = {}  # Will be populated dynamically by the screen

    def set_role_menu(self, role_name, menu_options):
        """
        Set menu options for a specific role

        Args:
            role_name: Name of the role (e.g., "Captain", "Navigator")
            menu_options: List of menu option strings
        """
        self.role_menus[role_name] = menu_options

    def open_role_menu(self, role_index):
        """Open the menu for a specific role"""
        if 0 <= role_index < len(self.roles):
            self.active_role = self.roles[role_index]

    def close_role_menu(self):
        """Close the active role menu and return to Bridge view"""
        self.active_role = None

    def get_active_menu_options(self):
        """Get menu options for the currently active role"""
        if self.active_role:
            return self.role_menus.get(self.active_role, [])
        return []

    def is_menu_active(self):
        """Check if a role menu is currently active"""
        return self.active_role is not None

    def render(self, screen, renderer):
        """Override to render title in border"""
        # Draw panel background and border
        super(GenericMenuPanel, self).render(screen, renderer)

        # Draw title in border based on current state
        title = f"{self.active_role}" if self.is_menu_active() else "Bridge"
        self.render_title(screen, renderer, title, self.config.title_color)

    def render_content_with_view_data(self, screen, renderer, game_state, coordinates, view_data):
        """
        Render crew roles or role menu with view data

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            coordinates: Optional (x, y) coordinate tuple (not used in this panel)
            view_data: Dictionary containing 'selected_role_index', 'selected_menu_index', etc.
        """
        if self.is_menu_active():
            # Update config and items for role menu
            self.config.title = f"{self.active_role}"
            self.config.items = self.get_active_menu_options()
            self.items = self.config.items  # Sync items with config
            # Render role menu
            selected_menu_index = view_data.get('selected_menu_index', 0)
            modified_view_data = {'selected_index': selected_menu_index}
            super().render_content_with_view_data(screen, renderer, game_state, coordinates, modified_view_data)
        else:
            # Update config and items for role list
            self.config.title = "Bridge"
            self.config.items = self.roles
            self.items = self.config.items  # Sync items with config
            # Render role list
            selected_role_index = view_data.get('selected_role_index', 0)
            modified_view_data = {'selected_index': selected_role_index}
            super().render_content_with_view_data(screen, renderer, game_state, coordinates, modified_view_data)

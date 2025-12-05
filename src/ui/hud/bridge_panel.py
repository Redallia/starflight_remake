"""
Bridge panel for displaying ship crew positions
Shows: Captain, Navigator, Engineer, Science, Communications, Medic
Can also display role-specific menus
"""
from ui.hud.hud_panel import HUDPanel


class BridgePanel(HUDPanel):
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
        super().__init__(x, y, width, height)

        # Define the six crew roles
        self.roles = [
            "Captain",
            "Navigator",
            "Engineer",
            "Science",
            "Communications",
            "Medic"
        ]

        # Role menu state
        self.active_role = None  # Which role's menu is active (None = showing role list)
        self.role_menus = self._initialize_role_menus()

    def _initialize_role_menus(self):
        """Initialize menu options for each role"""
        return {
            "Captain": ["Return to Bridge"],
            "Navigator": ["Leave Orbit", "Return to Bridge"],
            "Engineer": ["Return to Bridge"],
            "Science": ["Return to Bridge"],
            "Communications": ["Return to Bridge"],
            "Medic": ["Return to Bridge"]
        }

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

    def render_content(self, screen, renderer, game_state, coordinates=None):
        """
        Render crew roles in individual boxes (without selection highlight)

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            coordinates: Optional (x, y) coordinate tuple (not used in this panel)
        """
        self._render_roles(screen, renderer, selected_index=None)

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
            # Render role menu
            selected_menu_index = view_data.get('selected_menu_index', 0)
            self._render_role_menu(screen, renderer, selected_menu_index)
        else:
            # Render role list
            selected_index = view_data.get('selected_role_index', None)
            self._render_roles(screen, renderer, selected_index)

    def _render_roles(self, screen, renderer, selected_index=None):
        """
        Internal method to render crew roles in individual boxes

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            selected_index: Index of selected role (None for no selection)
        """
        import pygame

        content_x, content_y, content_width, content_height = self.get_content_rect()

        # Calculate box dimensions
        box_height = 35
        box_spacing = 5
        box_width = content_width - 20  # Leave margins on sides

        y_offset = content_y + 5

        # Render each role in its own box
        for i, role in enumerate(self.roles):
            is_selected = (i == selected_index)

            # Draw box background
            box_rect = pygame.Rect(
                content_x + 10,
                y_offset,
                box_width,
                box_height
            )

            # Background fill - highlight if selected
            if is_selected:
                pygame.draw.rect(screen, (60, 80, 100), box_rect)  # Brighter background
            else:
                pygame.draw.rect(screen, (30, 30, 40), box_rect)

            # Border - brighter if selected
            if is_selected:
                pygame.draw.rect(screen, (150, 180, 200), box_rect, 2)  # Thicker, brighter border
            else:
                pygame.draw.rect(screen, (80, 80, 100), box_rect, 1)

            # Draw role text centered vertically in box
            text_y = y_offset + (box_height - 16) // 2  # Center text vertically (assuming ~16px font height)
            text_color = (255, 255, 255) if is_selected else (200, 200, 220)
            renderer.draw_text(
                role,
                content_x + 20,
                text_y,
                color=text_color,
                font=renderer.default_font
            )

            y_offset += box_height + box_spacing

    def _render_role_menu(self, screen, renderer, selected_menu_index):
        """
        Render the active role's menu

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            selected_menu_index: Index of selected menu option
        """
        import pygame

        content_x, content_y, content_width, content_height = self.get_content_rect()

        # Draw role title at top
        title_y = content_y + 10
        renderer.draw_text(
            f"{self.active_role} Menu",
            content_x + 10,
            title_y,
            color=(100, 200, 255),
            font=renderer.large_font
        )

        # Get menu options for this role
        menu_options = self.get_active_menu_options()

        # Calculate menu box dimensions
        box_height = 35
        box_spacing = 5
        box_width = content_width - 20
        y_offset = content_y + 50  # Start below title

        # Render each menu option in its own box
        for i, option in enumerate(menu_options):
            is_selected = (i == selected_menu_index)

            # Draw box background
            box_rect = pygame.Rect(
                content_x + 10,
                y_offset,
                box_width,
                box_height
            )

            # Background fill - highlight if selected
            if is_selected:
                pygame.draw.rect(screen, (60, 80, 100), box_rect)
            else:
                pygame.draw.rect(screen, (30, 30, 40), box_rect)

            # Border - brighter if selected
            if is_selected:
                pygame.draw.rect(screen, (150, 180, 200), box_rect, 2)
            else:
                pygame.draw.rect(screen, (80, 80, 100), box_rect, 1)

            # Draw option text centered vertically in box
            text_y = y_offset + (box_height - 16) // 2
            text_color = (255, 255, 255) if is_selected else (200, 200, 220)
            renderer.draw_text(
                option,
                content_x + 20,
                text_y,
                color=text_color,
                font=renderer.default_font
            )

            y_offset += box_height + box_spacing

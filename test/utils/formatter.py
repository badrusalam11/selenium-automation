class Formatter:
    @staticmethod
    def str_to_bool(s: str) -> bool:
        """
        Convert a string to a boolean.

        Acceptable truthy values: 'true', '1', 'yes', 'y', 't'.
        Any other value will be considered False.

        Parameters:
            s (str): The input string.

        Returns:
            bool: True if the string is a truthy value, False otherwise.
        """
        return s.strip().lower() in ("true", "1", "yes", "y", "t")
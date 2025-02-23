class TimeConverter:
    @staticmethod
    def time_to_seconds(time_str: str | float, allow_negative: bool = False) -> float:
        """
        Convert a time string or number to seconds.
        Formats supported:
        - "5:05.5" or "5:05,5" -> 5 minutes and 5.5 seconds
        - "1:30:05.5" or "1:30:05,5" -> 1 hour, 30 minutes and 5.5 seconds
        - "5.5" or "5,5" -> 5.5 seconds
        - numeric value -> treated as seconds
        - negative values allowed if allow_negative is True
        
        Args:
            time_str: Time string in format "HH:MM:SS.ms", "MM:SS.ms" or "SS.ms", or seconds as float
            allow_negative: Whether to allow negative values (default: False)
            
        Returns:
            float: Time in seconds
            
        Raises:
            ValueError: If time format is invalid
        """
        # Handle numeric input
        if isinstance(time_str, (int, float)):
            value = float(time_str)
            if not allow_negative and value < 0:
                raise ValueError("Time cannot be negative")
            return value
        
        try:
            # Check if the time string starts with a minus
            is_negative = time_str.startswith('-')
            if is_negative:
                if not allow_negative:
                    raise ValueError("Time cannot be negative")
                time_str = time_str[1:]  # Remove the minus sign
            
            # Replace comma with dot for decimal points
            time_str = time_str.replace(',', '.')
            
            # Split by colon
            parts = time_str.split(':')
            
            if len(parts) > 3:
                raise ValueError("Invalid time format")
            
            try:
                # Convert the last part (which might contain decimal seconds)
                seconds = float(parts[-1])
                
                # Add minutes if present
                if len(parts) >= 2:
                    seconds += int(parts[-2]) * 60
                
                # Add hours if present
                if len(parts) == 3:
                    seconds += int(parts[0]) * 3600
            except (ValueError, IndexError):
                raise ValueError("Invalid time format")
            
            # Apply negative sign if needed
            if is_negative:
                seconds = -seconds
            
            return seconds
            
        except Exception as e:
            if isinstance(e, ValueError):
                raise e
            raise ValueError("Invalid time format")

    @staticmethod
    def seconds_to_time(seconds: float) -> str:
        """
        Convert seconds to time string format.
        
        Args:
            seconds (float): Time in seconds
            
        Returns:
            str: Time in format "HH:MM:SS.ms" or "MM:SS.ms"
        """
        if seconds < 0:
            raise ValueError("Time cannot be negative")
            
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        
        # Format with up to 3 decimal places, removing trailing zeros
        seconds_str = f"{seconds:.3f}".rstrip('0').rstrip('.')
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds_str:0>4}"
        elif minutes > 0:
            return f"{minutes}:{seconds_str:0>4}"
        else:
            return seconds_str 
# include this file at the top of your main file

# this file is to create a class to manage discord messages

# Decorators
# - Callback : Generic Function
# - Get : Get Function
# - Post : Post Function
# - GetPost : Get and Post Function

# Python Version : Python 3.12.1
# Date : 26-07-2024
# Software version : 0.1.1

# To get Message use the DiscordMessage class to pass in message
# it containes and embed_ and message_ to send in discord.py

from datetime import datetime
from discord import Embed, Colour
    
class DiscordMessage:
    # Constructor
    def __init__(self) -> None:
        self.embed_ : Embed | None = None
        self.message_ : str | None = None
        
    # SETTERS
    def CreateEmbed(self, *, title : str | None = None, description : str | None = None, colour : Colour = Colour.red(), url : str | None = None, timestamp : datetime = datetime.now()) -> None:
        self.embed_ = Embed(title=title, description=description, colour=colour, url=url, timestamp=timestamp)
        
    def EmbedAddField(self, *, name : str, value : str, inline : bool) -> None:
        self.embed_.add_field(name=name, value=value, inline=inline) # type: ignore
        
    def EmbedSetFooter(self, *, text : str, icon_url : str | None = None) -> None:
        self.embed_.set_footer(text=text, icon_url=icon_url) # type: ignore
    
    def EmbedSetImage(self, url : str) -> None:
        self.embed_.set_image(url=url) # type: ignore
    
    def EmbedSetThumbnail(self, url : str) -> None:
        self.embed_.set_thumbnail(url=url) # type: ignore
        
    def SetMessage(self, message : str) -> None:
        self.message_ = message
        
    # GETTERS
    def GetEmbed(self) -> Embed | None:
        return self.embed_
    
    def GetMessage(self) -> str | None:
        return self.message_
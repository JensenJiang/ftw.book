from simplelayout.types.common.interfaces import IPage
from zope.interface import Interface


class IBook(Interface):
    """Book marker interface.
    """


class IChapter(IPage):
    """Chapter marker interface.
    """


class IWithinBookLayer(Interface):
    """Request layer interface, automatically provided by request
    when traversing over book.
    """


class ILaTeXCodeInjectionEnabled(Interface):
    """Enables LaTeX code injection for admins on
    book-objects (chapters, SL-paragraphs).
    """

from Acquisition import aq_inner, aq_parent
from zope.interface import implements, Interface
from zope.component import adapts
from zope.dottedname.resolve import resolve
from Products.Archetypes import public
from Products.Archetypes import atapi
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from ftw.book import _
from ftw.book.interfaces import IBook, IChapter
from ftw.book.latex.layouts import register_book_layout
from ftw.pdfgenerator.layout.makolayout import MakoLayoutBase
from ftw.pdfgenerator.interfaces import IBuilder

class StringField(ExtensionField, public.StringField):
    pass

class IProceedingsLayoutSelectionLayer(Interface):
    """Request layer interface for selecting the proceedings layout.
    """

register_book_layout(IProceedingsLayoutSelectionLayer, _(u'Proceedings layout'))

class ProceedingsLayoutBookExtender(object):
    """Schema extender, adding the layout-specific(for ProccedingsLayout) fields for Book,
    including "edtior".
    """

    adapts(IBook)
    implements(ISchemaExtender)
    fields = [
        StringField(
            name='author',
            default='',
            required=False,
            widget=atapi.StringWidget(
                label = _(u'book_label_editor',default=u'Editor'),
            )
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):

        if self.context.isTemporary():
            return []

        layout_layer_name = getattr(self.context, 'latex_layout', None)
        if layout_layer_name:
            layout_layer = resolve(layout_layer_name)
            if layout_layer == IProceedingsLayoutSelectionLayer:
                return self.fields
        return []

class ProceedingsLayoutChapterExtender(object):
    """Schema extender, adding the layout-specific(for ProccedingsLayout) fields for Chapter
    in the first level, including "author".
    """
    adapts(IChapter)
    implements(ISchemaExtender)

    fields = [
        StringField(
            name='author',
            default='',
            required=False,
            widget=atapi.StringWidget(
                label = _(u'book_label_author',default=u'Author'),
            )
        ),
    ]
    def __init__(self, context):
        self.context = context

    def getFields(self):
        # Only chapters in the first level need to be extended
        if self.context.isTemporary():
            return []

        if not is_first_level_chapter(self.context):
            return []

        #Check Book's Layout
        par = aq_parent(aq_inner(self.context))
        layout_layer_name = getattr(par, 'latex_layout', None)
        if layout_layer_name:
            layout_layer = resolve(layout_layer_name)
            if layout_layer == IProceedingsLayoutSelectionLayer:
                return self.fields
        return []

class ProceedingsLayout(MakoLayoutBase):
    """A proceedings-like layout.
    """

    adapts(Interface, IProceedingsLayoutSelectionLayer, IBuilder)
    template_directories = []
    template_name = ''

def is_first_level_chapter(context):
    """Check if the context is Chapter in the first level of book
    """
    #If the context is None or it is not a chpater
    if context == None or not IChapter.providedBy(context): return False

    par = aq_parent(aq_inner(context))
    if par and IBook.providedBy(par): return True
    return False

from Acquisition import aq_inner, aq_parent
from zope.interface import implements, Interface
from zope.component import adapts
from zope.dottedname.resolve import resolve
from Products.Archetypes import public
from Products.Archetypes import atapi
from Products.CMFCore.utils import getToolByName
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from ftw.book import _
from ftw.book.latex.utils import get_raw_image_data
from ftw.book.helpers import BookHelper
from ftw.book.interfaces import IBook, IChapter
from ftw.book.latex.layouts import register_book_layout
from ftw.book.latex.defaultlayout import DefaultBookLayout
from ftw.pdfgenerator.layout.makolayout import MakoLayoutBase
from ftw.pdfgenerator.babel import get_preferred_babel_option_for_context
from ftw.pdfgenerator.interfaces import IBuilder
from zope.i18n import translate

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
        helper = BookHelper()
        if not helper.is_first_level_chapter(self.context):
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
    template_directories = ['proceedings_layout_templates']
    template_name = 'main.tex'

    def get_render_arguments(self):
        book = self.get_book()

        convert = self.get_converter().convert
        '''
        address = book.Schema().getField('author_address').get(book)
        address = convert(address.replace('\n', '<br />')).replace('\n', '')

        logo = book.Schema().getField('titlepage_logo').get(book)
        if logo and logo.data:
            logo_filename = 'titlepage_logo.jpg'
            self.get_builder().add_file(
                logo_filename,
                data=get_raw_image_data(logo.data))

            logo_width = book.Schema().getField(
                'titlepage_logo_width').get(book)
        else:
            logo_filename = False
            logo_width = 0
        '''
        args = {
            'context_is_book': self.context == book,
            'title': book.Title(),
            'use_titlepage': book.getUse_titlepage(),
            #'logo': logo_filename,
            #logo_width': logo_width,
            'use_toc': book.getUse_toc(),
            'use_lot': book.getUse_lot(),
            'use_loi': book.getUse_loi(),
            'use_index': book.getUse_index(),
            #'release': convert(book.Schema().getField('release').get(book)),
            'editor': convert(book.Schema().getField('author').get(book)),  #Editor
            #'authoraddress': address,
            'babel': get_preferred_babel_option_for_context(self.context),
            'index_title': self.get_index_title(),
        }
        return args

    def before_render_hook(self):
        self.use_package('hyperref',options = 'hidelinks')      #disable redbox around footnotes
        self.use_package('fancyhdr')
        self.use_package('babel')

        self.add_raw_template_file('simplebook.cls')

    def get_book(self):
        obj = self.context
        while obj and not IBook.providedBy(obj):
            obj = aq_parent(aq_inner(obj))
        return obj

    def get_index_title(self):
        context_language_method = getattr(self.context, 'getLanguage', None)
        if context_language_method:
            language_code = context_language_method()

        else:
            ltool = getToolByName(self.context, 'portal_languages')
            language_code = ltool.getPreferredLanguage()

        return translate(_(u'title_index', default=u'Index'),
                         target_language=language_code)

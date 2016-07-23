from ftw.book import _
from ftw.book.interfaces import ILayoutSettingsExtenderEnabled
from ftw.book.latex.proceedingslayout import IProceedingsLayoutSelectionLayer
from Products.Archetypes import atapi
from Products.Archetypes.public import StringField, DisplayList
from Products.DataGridField import DataGridField, DataGridWidget, Column, FixedRow
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from zope.dottedname.resolve import resolve
from zope.component import adapts
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass

class ExtensionStringField(ExtensionField, StringField):
    pass

class ExtensionDataGridField(ExtensionField, DataGridField):
    pass

class MySelectColumn(Column):
    """SelectColumn gets Vocabulary by invoking the method
    defined in the context class, but it makes more sense
    to provide Vocabulary when the class is created. More
    to see DataGridField.SelectColumn"""

    security = ClassSecurityInfo()
    def __init__(self, label, vocabulary, **kwargs):
        Column.__init__(self, label, **kwargs)
        self.vocabulary = vocabulary

    security.declarePublic('getVocabulary')
    def getVocabulary(self, instance):
        return self.vocabulary

    security.declarePublic('getMacro')
    def getMacro(self):
        return "datagrid_select_cell"

InitializeClass(MySelectColumn)

class LayoutSettingsExtender(object):
    adapts(ILayoutSettingsExtenderEnabled)
    implements(IOrderableSchemaExtender)

    _margin_list = DisplayList((
        ('2cm','2cm'),
        ('2.5cm','2.5cm'),
        ('3cm','3cm'),
        ('3.5cm','3.5cm'),
        ('4cm','4cm')
    ))

    fields = [
        ExtensionStringField(
            name = 'paper_size',
            schemata = 'Layout',
            default = 'a4paper',
            vocabulary = (
                _('a4paper', default = 'a4paper'),
                _('a5paper', default = 'a5paper'),
                _('b5paper', default = 'b5paper'),
                _('letterpaper', default = 'letterpaper'),
                _('legalpaper', default = 'legalpaper'),
                _('executivepaper', default = 'executivepaper'),
            ),
            widget = atapi.SelectionWidget(
                label = _(u'label_paper_size', default = u'Paper Size'),
                format = 'select'
            )
        ),
        ExtensionStringField(
            name = 'font_size',
            schemata = 'Layout',
            default = '10pt',
            vocabulary = (
                _('10pt', default = '10pt'),
                _('11pt', default = '11pt'),
                _('12pt', default = '12pt'),
            ),
            widget = atapi.SelectionWidget(
                label = _(u'label_font_size', default = u'Font Size'),
                format = 'select'
            )
        ),
        ExtensionDataGridField(
            name = 'Margin',
            schemata = 'Layout',
            widget = DataGridWidget(
                columns = {
                    'top': MySelectColumn(
                        label = 'top',
                        vocabulary = _margin_list
                    ),
                    'bottom': MySelectColumn(
                        label = 'bottom',
                        vocabulary = _margin_list
                    ),
                    'inner': MySelectColumn(
                        label = 'inner',
                        vocabulary = _margin_list
                    ),
                    'outer': MySelectColumn(
                        label = 'outer',
                        vocabulary = _margin_list
                    )
                },
            ),
            columns=('top','bottom','inner','outer'),
            fixed_row = [FixedRow(keyColumn = 'top', initialData = {'top': '2cm', 'bottom': '2cm', 'inner': '2cm', 'outer': '2cm'}),],
            allow_insert = False,
            allow_delete = False,
            allow_reorder = False,
        ),
    ]
    def getTestVo():
        return (_('a', default = 'a'),)
    def __init__(self,context):
        self.context = context

    def getFields(self):
        #Only Book has layout settings
        if self.context.isTemporary():
            return []

        layout_layer_name = getattr(self.context, 'latex_layout', None)
        if layout_layer_name:
            layout_layer = resolve(layout_layer_name)
            if layout_layer == IProceedingsLayoutSelectionLayer:
                return self.fields
        return []

    def getOrder(self, schematas):
        return schematas

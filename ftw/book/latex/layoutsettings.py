from ftw.book import _
from ftw.book.interfaces import ILayoutSettingsExtenderEnabled
from ftw.book.latex.proceedingslayout import IProceedingsLayoutSelectionLayer
from Products.Archetypes import atapi
from Products.Archetypes.public import StringField
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from zope.dottedname.resolve import resolve
from zope.component import adapts
from zope.interface import implements

class ExtensionStringField(ExtensionField, StringField):
    pass

class LayoutSettingsExtender(object):
    adapts(ILayoutSettingsExtenderEnabled)
    implements(IOrderableSchemaExtender)

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
    ]
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

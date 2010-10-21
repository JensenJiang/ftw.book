from plonegov.pdflatex.browser.converter import LatexCTConverter


class LinkLatexConverter(LatexCTConverter):

    def __call__(self, context, view):
        super(LinkLatexConverter, self).__call__(context, view)
        latex = []
        latex.append(r'\href{%s}{%s}' % (
            view.convert(self.context.remoteUrl),
            view.convert(self.context.Title())))
        return '\n'.join(latex)
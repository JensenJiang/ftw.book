\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{simplebook}[2016/06/23]

%Process Options
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions\relax

%Based on standard "book" class
\LoadClass{book}

% For graphicx, check if we are compiling under latex or pdflatex.
\ifx\pdftexversion\undefined
  \usepackage{graphicx}
\else
  \usepackage[pdftex]{graphicx}
\fi

% Set some sane defaults for section numbering depth and TOC depth.  You can
% reset these counters in your preamble.
%
\setcounter{secnumdepth}{2}
\setcounter{tocdepth}{1}

\newcommand{\chapterauthor}[1]{%
  {\parindent0pt\vspace*{-25pt}%
  \linespread{1.1}\large\scshape#1%
  \par\nobreak\vspace*{35pt}}
  \@afterheading%
}
\newcommand{\py@release}{}
\newcommand{\version}{}
\newcommand{\py@authoraddress}{}
\newcommand{\releasename}{Release}
\newcommand{\release}[1]{%
    \renewcommand{\py@release}{\releasename\space\version}
    \renewcommand{\version}{#1}}
\newcommand{\authoraddress}[1]{%
    \renewcommand{\py@authoraddress}{#1}}

% Redefine includgraphics for avoiding images larger than the screen size
% If the size is not specified.
\let\py@Oldincludegraphics\includegraphics
\newbox\image@box%
\newdimen\image@width%
\renewcommand\includegraphics[2][\@empty]{%
  \ifx#1\@empty%
    \setbox\image@box=\hbox{\py@Oldincludegraphics{#2}}%
    \image@width\wd\image@box%
    \ifdim \image@width>\linewidth%
      \setbox\image@box=\hbox{\py@Oldincludegraphics[width=\linewidth]{#2}}%
      \box\image@box%
    \else%
      \py@Oldincludegraphics{#2}%
    \fi%
  \else%
    \py@Oldincludegraphics[#1]{#2}%
  \fi%
}

\renewcommand{\maketitle}{%
    \begin{titlepage}%
        \let\footnotesize\small
        \let\footnoterule\relax
        \let\footnote\thanks
        \null\vfil
        \vskip 60\p@
        \begin{center}%
            {\Huge \@title \par}%
            {\em\LARGE \py@release \par}
            \vskip 3em%
            {\large
                \lineskip .75em%
                \begin{tabular}[t]{c}%
                    \@author
                \end{tabular}\par}%

            {\large
            \@date \par
            \py@authoraddress \par
            }%
            \booklogo%
        \end{center}%
        \@thanks
    \end{titlepage}%
}

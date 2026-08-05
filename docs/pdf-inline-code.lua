-- PDF only: wrap inline code spans in \iccolor{...} (defined in
-- header_extra.tex) so they get the same pink-on-light-grey chip look
-- as the HTML build's `code:not(pre code)` rule. Pandoc's own escaping
-- of the code text is untouched -- we only add raw LaTeX before/after
-- the Code element, so this never touches the `\texttt{...}` that the
-- filename-caption feature emits separately (that's raw LaTeX text,
-- not a Code AST node, so it never passes through this filter).
function Code(el)
  if quarto.doc.is_format("latex") then
    return {
      pandoc.RawInline("latex", "\\iccolor{"),
      el,
      pandoc.RawInline("latex", "}"),
    }
  end
end

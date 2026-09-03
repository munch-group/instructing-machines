-- PDF only. Tightens the gap between an "Exercise" heading and its
-- badge paragraph (`SOLO`/`AI: <Role>`, always its own paragraph
-- right below the heading in the source) to about a third of KOMA's
-- normal heading-to-paragraph gap, by inserting a \vspace directly
-- before that paragraph. This is scoped to that one paragraph rather
-- than done via KOMA's own subsubsection afterskip, because a
-- negative afterskip there corrupted the heading's own number/title
-- layout.
local function is_badge_para(block)
  return block.t == "Para" and #block.content == 1 and block.content[1].t == "Code"
end

function Blocks(blocks)
  if not quarto.doc.is_format("latex") then
    return blocks
  end

  local out = {}
  for i, block in ipairs(blocks) do
    if is_badge_para(block) and blocks[i - 1] and blocks[i - 1].t == "Header" and blocks[i - 1].level == 4 then
      table.insert(out, pandoc.RawBlock("latex", "\\vspace{-14pt}"))
    end
    table.insert(out, block)
  end
  return pandoc.Blocks(out)
end

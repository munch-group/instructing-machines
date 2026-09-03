function Header(el)
  -- Change '2' to whichever heading level you want to unnumber
  if el.level == 2 then
    table.insert(el.classes, "unnumbered")
  end
  if el.level == 3 then
    table.insert(el.classes, "unnumbered")
  end  
  return el
end

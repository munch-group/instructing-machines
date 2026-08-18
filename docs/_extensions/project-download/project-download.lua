-- The margin "Download project" control, the companion to notebook-download.
--
-- notebook-download embeds the chapter's own .ipynb as a base64 data URI,
-- which works because a notebook is tens of kilobytes. A project is a folder,
-- and one of them carries a 5 MB genome, so this one links to the zip that
-- scripts/build_student_folder.py publishes alongside the book instead. The
-- button is the same button; only the delivery differs.
--
-- It renders on a project chapter and nowhere else. A chapter is a project
-- chapter when it is called <name>-project and project-files/<name>project
-- actually holds a test file, so a chapter written for a project that does not
-- exist yet (or one held out of the book) silently gets no button.

local str = pandoc.utils.stringify

local function ensureHtmlDeps()
  quarto.doc.add_html_dependency({
    name = "project-download",
    version = "1.0.0",
    stylesheets = {"resources/css/project-download.css"}
  })
end

local function optional(arg, default)
  if arg == nil or arg == ""
  then
    return default
  else
    return arg
  end
end

local function readable(path)
  local fh = io.open(path, "r")
  if fh == nil then
    return false
  end
  fh:close()
  return true
end

-- "…/docs/projects/alignment-project.qmd" -> "alignmentproject", or nil
local function project_for(file_path)
  if not file_path then
    return nil
  end
  local basename = pandoc.path.filename(file_path)
  local stem = pandoc.path.split_extension(basename)
  local prefix = stem:match("^(.+)%-project$")
  if not prefix then
    return nil
  end
  local name = prefix:gsub("[-_]", "") .. "project"
  local directory = pandoc.path.directory(file_path)
  local test_file = pandoc.path.join({directory, "..", "..", "project-files",
                                      name, "test_" .. name .. ".py"})
  if not readable(test_file) then
    return nil
  end
  return name
end

return {
  ['project-download'] = function(args, kwargs, meta)
    local name = project_for(quarto.doc.input_file)
    if not name then
      return pandoc.Null()
    end

    if not (quarto.doc.is_format("html:js") and quarto.doc.has_bootstrap()) then
      return pandoc.Null()
    end

    local archive = name .. ".zip"
    -- The chapters render into _book/projects/ and the zips are published to
    -- _book/project-files/, so this is one step up and across. It is written
    -- relative rather than from the site root because the book is served from
    -- a subpath (munch-group.org/instructing-machines).
    local href = "../project-files/" .. archive

    local btn_label = " " .. optional(str(kwargs["label"]), "Download project") .. " "
    local btn_type = optional(str(kwargs["type"]), "default")
    local icon = optional(str(kwargs["icon"]), "download")
    local class = " " .. optional(str(kwargs["class"]), "")
    local dname = optional(str(kwargs["dname"]), archive)

    ensureHtmlDeps()

    local button =
        "<button class=\"btn btn-" .. btn_type .. " downloadthis " ..
        class .. "\"" ..
        "><i class=\"bi bi-" .. icon .. "\"" .. "></i>" ..
        btn_label ..
        "</button>"

    return pandoc.RawInline('html',
      "<a href=\"" .. href .. "\" download=\"" .. dname .. "\">" .. button .. "</a>"
    )
  end
}

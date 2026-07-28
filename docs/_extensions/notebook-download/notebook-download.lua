local str = pandoc.utils.stringify

local function ensureHtmlDeps()
  quarto.doc.add_html_dependency({
    name = "notebook-download",
    version = "1.0.0",
    stylesheets = {"resources/css/notebook-download.css"}
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

return {
  ['notebook-download'] = function(args, kwargs, meta)
    local file_path = quarto.doc.input_file

    -- Only chapters authored as notebooks have a source .ipynb students
    -- can run; skip silently everywhere else (index, plain .qmd/.md pages).
    if not file_path or not file_path:match("%.ipynb$") then
      return pandoc.Null()
    end

    local fh = io.open(file_path, "rb")
    if not fh then
      io.stderr:write("notebook-download: cannot open " .. file_path .. " | skipping\n")
      return pandoc.Null()
    end

    local contents = fh:read("*all")
    fh:close()

    local basename = pandoc.path.filename(file_path)
    local stem = pandoc.path.split_extension(basename)

    local dname = optional(str(kwargs["dname"]), stem)
    local dfilename = dname .. ".ipynb"
    local btn_label = " " .. optional(str(kwargs["label"]), "Download notebook") .. " "
    local btn_type = optional(str(kwargs["type"]), "default")
    local icon = optional(str(kwargs["icon"]), "download")
    local class = " " .. optional(str(kwargs["class"]), "")
    local rand = "dnldts" .. str(math.random(1, 65000))
    local id = optional(str(kwargs["id"]), rand)

    local b64_encoded = quarto.base64.encode(contents)
    local data_uri = "data:application/x-ipynb+json;base64," .. b64_encoded

    local js = [[fetch('%s').then(res => res.blob()).then(blob => {
    const downloadURL = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    document.body.appendChild(a);
    a.href = downloadURL;
    a.download = '%s'; a.click();
    window.URL.revokeObjectURL(downloadURL);
    document.body.removeChild(a);
      });]]

    local clicked = js:format(data_uri, dfilename)

    local button =
        "<button class=\"btn btn-" .. btn_type .. " downloadthis " ..
        class .. "\"" ..
        " id=\"" .. id .. "\"" ..
        "><i class=\"bi bi-" .. icon .. "\"" .. "></i>" ..
        btn_label ..
        "</button>"

    if quarto.doc.is_format("html:js") and quarto.doc.has_bootstrap()
    then
      ensureHtmlDeps()
      return pandoc.RawInline('html',
        "<a href=\"#" .. id .. "\"" ..
        " onclick=\"" .. clicked .. "\">" .. button .. "</a>"
      )
    else
      return pandoc.Null()
    end
  end
}

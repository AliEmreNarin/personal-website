Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
  next unless doc.output_ext == ".html"
  next unless doc.output.include?("</body>")

  baseurl = doc.site.config["baseurl"] || ""
  tag = %(<script src="#{baseurl}/assets/js/dog.js"></script>)
  doc.output = doc.output.sub("</body>", "#{tag}\n</body>")
end

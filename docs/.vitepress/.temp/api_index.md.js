import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"API reference","description":"Complete generated C++ and Python API reference for kiyosi.","frontmatter":{"description":"Complete generated C++ and Python API reference for kiyosi."},"headers":[],"relativePath":"api/index.md","filePath":"api/index.md"}');
const _sfc_main = { name: "api/index.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="api-reference" tabindex="-1">API reference <a class="header-anchor" href="#api-reference" aria-label="Permalink to &quot;API reference&quot;">​</a></h1><p>This reference is generated from the library&#39;s public C++ headers and installed Python API.</p><p>Library version: <strong>0.10.0</strong>.</p><ul><li><a href="./cpp/">C++ API</a> — declarations and Doxygen comments from every public header.</li><li><a href="./python/">Python API</a> — public exports, signatures, members, and docstrings.</li></ul><div class="warning custom-block"><p class="custom-block-title">Alpha API</p><p>Kiyosi currently makes no backward-compatibility guarantees. Regenerate these pages after updating the library.</p></div></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("api/index.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const index = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  index as default
};

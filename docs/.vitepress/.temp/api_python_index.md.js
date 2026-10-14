import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Python API reference","description":"Complete Python API generated from kiyosi runtime docstrings.","frontmatter":{"description":"Complete Python API generated from kiyosi runtime docstrings."},"headers":[],"relativePath":"api/python/index.md","filePath":"api/python/index.md"}');
const _sfc_main = { name: "api/python/index.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="python-api-reference" tabindex="-1">Python API reference <a class="header-anchor" href="#python-api-reference" aria-label="Permalink to &quot;Python API reference&quot;">​</a></h1><p>The pages below are generated from each public module&#39;s exports (<code>__all__</code> when declared, otherwise public names), runtime signatures, and docstrings, including native nanobind objects.</p><ul><li><a href="./kiyosi.html"><code>kiyosi</code></a></li><li><a href="./kiyosi-instruments.html"><code>kiyosi.instruments</code></a></li><li><a href="./kiyosi-market.html"><code>kiyosi.market</code></a></li><li><a href="./kiyosi-pricing.html"><code>kiyosi.pricing</code></a></li></ul></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("api/python/index.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const index = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  index as default
};

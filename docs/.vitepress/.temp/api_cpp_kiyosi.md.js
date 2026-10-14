import { ssrRenderAttrs, ssrRenderStyle } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"<kiyosi/kiyosi.hpp>","description":"C++ API declarations from kiyosi/kiyosi.hpp.","frontmatter":{"description":"C++ API declarations from kiyosi/kiyosi.hpp.","outline":[2,4]},"headers":[],"relativePath":"api/cpp/kiyosi.md","filePath":"api/cpp/kiyosi.md"}');
const _sfc_main = { name: "api/cpp/kiyosi.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="kiyosi-kiyosi-hpp" tabindex="-1"><code>&lt;kiyosi/kiyosi.hpp&gt;</code> <a class="header-anchor" href="#kiyosi-kiyosi-hpp" aria-label="Permalink to &quot;\`&lt;kiyosi/kiyosi.hpp&gt;\`&quot;">​</a></h1><div class="language-cpp vp-adaptive-theme"><button title="复制代码" class="copy"></button><span class="lang">cpp</span><pre class="shiki shiki-themes github-light-high-contrast github-dark-high-contrast vp-code" tabindex="0"><code><span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#A0111F", "--shiki-dark": "#FF9492" })}">#include</span><span style="${ssrRenderStyle({ "--shiki-light": "#032563", "--shiki-dark": "#ADDCFF" })}"> &lt;kiyosi/kiyosi.hpp&gt;</span></span></code></pre></div><p>Thread safety: Unless documented otherwise, operations on distinct objects and concurrent const operations on the same object are safe. An object must remain alive and must not be moved from, assigned to, or otherwise mutated during concurrent access. Concurrent access involving mutation requires external synchronization.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("api/cpp/kiyosi.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const kiyosi = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  kiyosi as default
};

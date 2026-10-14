import { ssrRenderAttrs, ssrRenderStyle } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"<kiyosi/market/calendars/sse.hpp>","description":"C++ API declarations from kiyosi/market/calendars/sse.hpp.","frontmatter":{"description":"C++ API declarations from kiyosi/market/calendars/sse.hpp.","outline":[2,4]},"headers":[],"relativePath":"api/cpp/market-calendars-sse.md","filePath":"api/cpp/market-calendars-sse.md"}');
const _sfc_main = { name: "api/cpp/market-calendars-sse.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="kiyosi-market-calendars-sse-hpp" tabindex="-1"><code>&lt;kiyosi/market/calendars/sse.hpp&gt;</code> <a class="header-anchor" href="#kiyosi-market-calendars-sse-hpp" aria-label="Permalink to &quot;\`&lt;kiyosi/market/calendars/sse.hpp&gt;\`&quot;">​</a></h1><div class="language-cpp vp-adaptive-theme"><button title="复制代码" class="copy"></button><span class="lang">cpp</span><pre class="shiki shiki-themes github-light-high-contrast github-dark-high-contrast vp-code" tabindex="0"><code><span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#A0111F", "--shiki-dark": "#FF9492" })}">#include</span><span style="${ssrRenderStyle({ "--shiki-light": "#032563", "--shiki-dark": "#ADDCFF" })}"> &lt;kiyosi/market/calendars/sse.hpp&gt;</span></span></code></pre></div><h2 id="sse-calendar" tabindex="-1"><code>sse_calendar</code> <a class="header-anchor" href="#sse-calendar" aria-label="Permalink to &quot;\`sse_calendar\`&quot;">​</a></h2><div class="language-cpp vp-adaptive-theme"><button title="复制代码" class="copy"></button><span class="lang">cpp</span><pre class="shiki shiki-themes github-light-high-contrast github-dark-high-contrast vp-code" tabindex="0"><code><span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#702C00", "--shiki-dark": "#FFB757" })}">TradingCalendar</span><span style="${ssrRenderStyle({ "--shiki-light": "#702C00", "--shiki-dark": "#FFB757" })}"> kiyosi</span><span style="${ssrRenderStyle({ "--shiki-light": "#0E1116", "--shiki-dark": "#F0F3F6" })}">::</span><span style="${ssrRenderStyle({ "--shiki-light": "#622CBC", "--shiki-dark": "#DBB7FF" })}">sse_calendar</span><span style="${ssrRenderStyle({ "--shiki-light": "#0E1116", "--shiki-dark": "#F0F3F6" })}">()</span></span></code></pre></div><p>Shanghai Stock Exchange: weekdays excluding recorded XSHG and forecast holidays. The table spans 1991..2099; dates beyond the upstream list are estimates. Outside that span, queries fall back to a holiday-unaware weekday calendar. <strong>Returns:</strong> The SSE trading calendar with a 243-day annualization basis.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("api/cpp/market-calendars-sse.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const marketCalendarsSse = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  marketCalendarsSse as default
};

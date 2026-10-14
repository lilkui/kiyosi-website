import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"简介","description":"了解 kiyosi 的功能、定价流程和当前模型的适用范围。","frontmatter":{"description":"了解 kiyosi 的功能、定价流程和当前模型的适用范围。"},"headers":[],"relativePath":"guide/introduction.md","filePath":"guide/introduction.md"}');
const _sfc_main = { name: "guide/introduction.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="简介" tabindex="-1">简介 <a class="header-anchor" href="#简介" aria-label="Permalink to &quot;简介&quot;">​</a></h1><p>Kiyosi 是一个开源衍生品定价库，支持普通期权、奇异期权和结构化产品。核心功能用 C++23 实现，主要通过 Python API 使用。</p><div class="warning custom-block"><p class="custom-block-title">早期开发阶段</p><p>本文档对应 <strong>kiyosi 0.10.0</strong>。项目处于 Alpha 阶段，API 可能发生变化，不保证向后兼容。</p></div><h2 id="how-pricing-fits-together" tabindex="-1">定价流程 <a class="header-anchor" href="#how-pricing-fits-together" aria-label="Permalink to &quot;定价流程 {#how-pricing-fits-together}&quot;">​</a></h2><p>定价需要三个对象：</p><ol><li><strong>金融工具</strong>：描述合约，包括行权价、日期和收益类型。</li><li><strong>市场上下文</strong>：提供模型参数、标的现价和估值时点。</li><li><strong>定价引擎</strong>：根据金融工具和市场上下文，使用指定方法计算价格。</li></ol><p>Python 的 <code>price()</code> 直接返回价格数值。需要计算希腊字母风险指标（Greeks）时，调用 <code>price_with_greeks()</code> 并指定指标；该方法返回的 <code>PricingResult</code> 包含价格和所选 Greeks。</p><p>不同金融工具支持的定价方法不同，详见<a href="./engines.html">定价引擎</a>。</p><h2 id="model-scope" tabindex="-1">模型适用范围 <a class="header-anchor" href="#model-scope" aria-label="Permalink to &quot;模型适用范围 {#model-scope}&quot;">​</a></h2><p>当前模型采用 Black-Scholes-Merton 参数，无风险利率、股息率和波动率均为常数。API 尚不支持波动率曲面和利率曲线。</p><p>库中还提供交易日历和观察日程构建工具，包含上交所节假日安排。支持的产品包括欧式期权、美式期权、累购产品、凤凰产品及多种雪球结构。</p><h2 id="validation" tabindex="-1">结果验证 <a class="header-anchor" href="#validation" aria-label="Permalink to &quot;结果验证 {#validation}&quot;">​</a></h2><p>Kiyosi 的定价测试以 QuantLib 独立生成的数值为基准。QuantLib 用于生成参考值和维护日历；C++ 核心库的构建和运行均不依赖 QuantLib。</p><h2 id="where-to-begin" tabindex="-1">从哪里开始 <a class="header-anchor" href="#where-to-begin" aria-label="Permalink to &quot;从哪里开始 {#where-to-begin}&quot;">​</a></h2><ul><li><a href="./installation.html">安装 Python 包</a>，快速开始定价。</li><li><a href="./first-price.html">完成首次定价</a>，运行一个完整示例。</li><li><a href="./../cpp/building.html">构建 C++ 库</a>，直接使用原生 API。</li></ul><p>来源：<a href="https://github.com/lilkui/kiyosi/blob/main/README.md" target="_blank" rel="noreferrer">kiyosi README</a>。Kiyosi 采用 <a href="https://github.com/lilkui/kiyosi/blob/main/LICENSE.txt" target="_blank" rel="noreferrer">MIT 许可证</a>。</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("guide/introduction.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const introduction = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  introduction as default
};

/* Wind & snow load calculator — UI + logic */
const PERIOD_COEFF = { 10: 0.724, 25: 0.907, 50: 1.0, 100: 1.184 };
const KN_TO_PA = 1000;
const KN_TO_KGF = 101.9716;
const KN_TO_PSF = 20.8854;

const LANG = {
    zh: {
        mainTitle: "全球风压雪压计算评估工具",
        subTitle: "GB 50009-2012 · 全球77国 · 地图点选 / 模糊搜索",
        returnPeriodTip: "25年重现期换算系数：0.907",
        labelContinent: "洲",
        labelCountry: "国家/地区",
        labelPeriod: "设计重现期",
        labelProvince: "省份/大区",
        labelCity: "城市/城区",
        labelSearch: "搜索城市（模糊匹配）",
        searchPlaceholder: "输入城市名，如：北京、纽约、东京…",
        mapHint: "Natural Earth 地图 · 悬停选择洲 · 双击或「全屏」放大",
        mapLoading: "地图加载中…",
        btnMapFullscreen: "⛶ 全屏",
        mapModalTitle: "世界地图 — 选择洲",
        mapModalCloseHint: "按 Esc 关闭",
        btnCalc: "开始计算",
        countTip: "加载中…",
        textCode: "适用规范",
        textWind50: "50年基准风压",
        textSnow50: "50年基准雪压",
        textWindCur: "当前重现期风压",
        textSnowCur: "当前重现期雪压",
        unitTitle: "多单位换算",
        textWPa: "风压 Pa", textWKgf: "风压 kgf/m²", textWPsf: "风压 psf",
        textSPa: "雪压 Pa", textSKgf: "雪压 kgf/m²", textSPsf: "雪压 psf",
        noteText: "国内：GB 50009-2012 附录E.5；国外：各国规范50年基准参考值。正式工程以当地现行规范为准。\n1 kN/m² = 1000 Pa ≈ 101.97 kgf/m² ≈ 20.885 psf",
        sourceText: "编制单位：浙江中南新能源有限公司技术部 | 作者：董子凌 | GB 50009-2012 + 全球77国风/雪荷载规范",
        errContinent: "请先选择洲",
        errProvince: "请选择省份/大区",
        errCity: "请选择城市/城区",
        errNoData: "暂无该地区数据",
        selectContinent: "— 选择洲 —",
        selectCountry: "— 选择国家 —",
        selectProvince: "— 选择省份/大区 —",
        selectCity: "— 选择城市 —",
        chinaLabel: "中国（GB 50009-2012）",
        noSearch: "无匹配结果",
        resultPlaceholder: "选择地点后点击「开始计算」",
        riskHigh: "高风险", riskMid: "中风险", riskLow: "低风险",
        aiTitle: "AI 智能设计推荐",
        coastalWind: "沿海/高风压：按50年荷载验算抗风、抗倾覆；盐雾区镀锌≥85μm。",
        heavySnow: "大雪区：雪荷载控制，验算地基与防冻；镀锌≥65μm。",
        midLoad: "中等荷载：按通用规范设计，镀锌≥65μm。",
        lowLoad: "低荷载区：按基础规范即可，镀锌≥65μm。",
        stdTip: "规范：{std}（参考值，正式设计以当地规范为准）",
        conclusion: "{city}：【{risk}】",
    },
    en: {
        mainTitle: "Wind & Snow Load Calculator",
        subTitle: "GB 50009-2012 · 77 countries · Map & fuzzy search",
        returnPeriodTip: "25-year coefficient: 0.907",
        labelContinent: "Continent",
        labelCountry: "Country",
        labelPeriod: "Return period",
        labelProvince: "Region",
        labelCity: "City",
        labelSearch: "Search city",
        searchPlaceholder: "Type city name: Beijing, New York, Tokyo…",
        mapHint: "Natural Earth · hover to select · dbl-click or Fullscreen",
        mapLoading: "Loading map…",
        btnMapFullscreen: "⛶ Fullscreen",
        mapModalTitle: "World Map — Select Continent",
        mapModalCloseHint: "Press Esc to close",
        btnCalc: "Calculate",
        countTip: "Loading…",
        textCode: "Code",
        textWind50: "50-yr wind",
        textSnow50: "50-yr snow",
        textWindCur: "Design wind",
        textSnowCur: "Design snow",
        unitTitle: "Units",
        textWPa: "Wind Pa", textWKgf: "Wind kgf/m²", textWPsf: "Wind psf",
        textSPa: "Snow Pa", textSKgf: "Snow kgf/m²", textSPsf: "Snow psf",
        noteText: "China: GB 50009-2012 App. E.5; overseas: 50-yr reference per national codes.\n1 kN/m² = 1000 Pa ≈ 101.97 kgf/m² ≈ 20.885 psf",
        sourceText: "Zhejiang Zhongnan New Energy Co., Ltd. Tech Dept. | Author: Dong Ziling | GB 50009-2012 + 77 countries",
        errContinent: "Select a continent first",
        errProvince: "Select region",
        errCity: "Select city",
        errNoData: "No data",
        selectContinent: "— Continent —",
        selectCountry: "— Country —",
        selectProvince: "— Region —",
        selectCity: "— City —",
        chinaLabel: "China (GB 50009-2012)",
        noSearch: "No matches",
        resultPlaceholder: "Select location and click Calculate",
        riskHigh: "High", riskMid: "Medium", riskLow: "Low",
        aiTitle: "AI Design Recommendation",
        coastalWind: "Coastal/high wind: use 50-yr loads; galvanizing ≥85μm in salt areas.",
        heavySnow: "Heavy snow: snow governs; check foundation; galvanizing ≥65μm.",
        midLoad: "Medium loads: general code; galvanizing ≥65μm.",
        lowLoad: "Low loads: basic design; galvanizing ≥65μm.",
        stdTip: "Code: {std} (reference only)",
        conclusion: "{city}: 【{risk}】",
    },
};

const COASTAL_CITIES = [
    "纽约","波士顿","迈阿密","洛杉矶","西雅图","休斯顿","温哥华","悉尼","墨尔本","达尔文",
    "东京","大阪","釜山","新加坡","迪拜","孟买","马尼拉","雅加达","曼谷","胡志明市","吉隆坡",
    "开普敦","拉各斯","蒙巴萨","科伦坡","里斯本","马赛","巴塞罗那","汉堡","哥本哈根",
    "上海","杭州","宁波","温州","福州","厦门","泉州","广州","深圳","珠海","汕头","湛江",
    "青岛","大连","连云港","盐城","海口","三亚","北海","防城港","钦州",
];

let currentLang = "zh";
let selectedContinent = "";
let searchIndex = [];
let searchTimer = null;
let cachedMapSvg = null;
let mapZoomLevel = 1;
const MAP_ZOOM_MIN = 0.6;
const MAP_ZOOM_MAX = 2.5;
const MAP_ZOOM_STEP = 0.2;

function t(key) {
    return LANG[currentLang][key];
}

function countChinaCities() {
    let n = 0;
    for (const p in DATA) n += Object.keys(DATA[p]).length;
    return n;
}

function countGlobalCities() {
    let n = 0;
    for (const c in GLOBAL_DATA)
        for (const r in GLOBAL_DATA[c].regions)
            n += Object.keys(GLOBAL_DATA[c].regions[r]).length;
    return n;
}

function updateCountTip() {
    const cc = countChinaCities();
    const gc = Object.keys(GLOBAL_DATA).length;
    const gct = countGlobalCities();
    document.getElementById("countTip").innerText = currentLang === "zh"
        ? `国内 ${cc} 城 · 全球 ${gc} 国 ${gct} 城`
        : `China ${cc} · ${gc} countries ${gct} cities`;
}

function getCountryName(code) {
    if (code === "china") return currentLang === "zh" ? "中国" : "China";
    return GLOBAL_DATA[code]?.name[currentLang] || code;
}

function getLoadData(country, prov, city) {
    if (country === "china") return DATA[prov]?.[city] || null;
    return GLOBAL_DATA[country]?.regions[prov]?.[city] || null;
}

function countriesInContinent(cont) {
    const list = [];
    if (cont === "asia")
        list.push({ code: "china", label: t("chinaLabel") });
    for (const code of Object.keys(GLOBAL_DATA).sort((a, b) =>
        GLOBAL_DATA[a].name[currentLang].localeCompare(
            GLOBAL_DATA[b].name[currentLang], currentLang === "zh" ? "zh" : "en"))) {
        if (COUNTRY_CONTINENT[code] === cont)
            list.push({
                code,
                label: `${GLOBAL_DATA[code].name[currentLang]}（${GLOBAL_DATA[code].code}）`,
            });
    }
    return list;
}

function buildContinentSelect() {
    const sel = document.getElementById("continent");
    const prev = sel.value || selectedContinent;
    sel.innerHTML = `<option value="">${t("selectContinent")}</option>`;
    for (const id of Object.keys(CONTINENT_INFO)) {
        const name = CONTINENT_INFO[id][currentLang === "zh" ? "zh" : "en"];
        sel.add(new Option(name, id));
    }
    if (prev && CONTINENT_INFO[prev]) sel.value = prev;
    selectedContinent = sel.value;
}

function buildCountrySelect() {
    const sel = document.getElementById("country");
    const cont = document.getElementById("continent").value;
    const prev = sel.value;
    sel.innerHTML = `<option value="">${t("selectCountry")}</option>`;
    sel.disabled = !cont;
    if (!cont) return;
    for (const item of countriesInContinent(cont))
        sel.add(new Option(item.label, item.code));
    if (prev && [...sel.options].some((o) => o.value === prev)) sel.value = prev;
}

function onContinentChange(fromMap) {
    selectedContinent = document.getElementById("continent").value;
    if (!fromMap) highlightContinentOnMap(selectedContinent);
    buildCountrySelect();
    updateRegions();
    syncContinentTabs();
}

function onCountryChange() {
    updateRegions();
}

function updateRegions() {
    const country = document.getElementById("country").value;
    const provSel = document.getElementById("province");
    const citySel = document.getElementById("city");
    provSel.innerHTML = `<option value="">${t("selectProvince")}</option>`;
    citySel.innerHTML = `<option value="">${t("selectCity")}</option>`;
    provSel.disabled = !country;
    citySel.disabled = true;

    if (country === "china") {
        for (const prov in DATA) provSel.add(new Option(prov, prov));
    } else if (GLOBAL_DATA[country]) {
        for (const area in GLOBAL_DATA[country].regions)
            provSel.add(new Option(area, area));
    }
}

function updateCities() {
    const country = document.getElementById("country").value;
    const prov = document.getElementById("province").value;
    const citySel = document.getElementById("city");
    citySel.innerHTML = `<option value="">${t("selectCity")}</option>`;
    citySel.disabled = !prov;
    if (!prov) return;

    if (country === "china" && DATA[prov]) {
        for (const c in DATA[prov]) citySel.add(new Option(c, c));
    } else if (GLOBAL_DATA[country]?.regions[prov]) {
        for (const c in GLOBAL_DATA[country].regions[prov])
            citySel.add(new Option(c, c));
    }
}

function updatePeriodTip() {
    const period = document.getElementById("returnPeriod").value;
    const coeff = PERIOD_COEFF[period];
    const label = currentLang === "zh" ? "重现期换算系数" : "Coefficient";
    document.getElementById("returnPeriodTip").innerText =
        `${period}${currentLang === "zh" ? "年" : "-yr"} ${label}：${coeff}`;
}

/* —— Map —— */
function highlightContinentOnMap(contId, tooltipText) {
    document.querySelectorAll(".map-wrap").forEach((wrap) => {
        wrap.classList.toggle("has-selection", !!contId);
    });

    document.querySelectorAll(".continent-path").forEach((el) => {
        const c = el.dataset.continent;
        el.classList.toggle("active", c === contId && !!contId);
    });
    document.querySelectorAll(".continent-tab").forEach((btn) => {
        btn.classList.toggle("active", btn.dataset.continent === contId);
    });

    const name =
        tooltipText ||
        (contId && CONTINENT_INFO[contId]
            ? CONTINENT_INFO[contId][currentLang === "zh" ? "zh" : "en"]
            : "");
    document.querySelectorAll(".map-tooltip").forEach((tip) => {
        if (name) {
            tip.textContent = name;
            tip.classList.add("show");
        } else {
            tip.classList.remove("show");
        }
    });
}

function selectContinent(contId, closeModalOnSelect) {
    document.getElementById("continent").value = contId;
    onContinentChange(true);
    highlightContinentOnMap(contId);
    if (closeModalOnSelect) closeMapModal();
}

function applyMapZoom() {
    const scale = mapZoomLevel.toFixed(2);
    const label = Math.round(mapZoomLevel * 100) + "%";
    ["mapZoomInner", "mapModalZoomInner"].forEach((id) => {
        const el = document.getElementById(id);
        if (el) el.style.transform = `scale(${scale})`;
    });
    const lbl = document.getElementById("mapZoomLabel");
    const lblM = document.getElementById("mapModalZoomLabel");
    if (lbl) lbl.textContent = label;
    if (lblM) lblM.textContent = label;
}

function changeMapZoom(delta) {
    mapZoomLevel = Math.min(
        MAP_ZOOM_MAX,
        Math.max(MAP_ZOOM_MIN, Math.round((mapZoomLevel + delta) * 10) / 10),
    );
    applyMapZoom();
}

function resetMapZoom() {
    mapZoomLevel = 1;
    applyMapZoom();
}

function bindMapPaths(root, onSelect) {
    if (!root) return;
    root.querySelectorAll(".continent-path").forEach((path) => {
        const cont = path.dataset.continent;
        path.addEventListener("mouseenter", () => {
            highlightContinentOnMap(cont);
        });
        path.addEventListener("mouseleave", () => {
            highlightContinentOnMap(document.getElementById("continent").value);
        });
        path.addEventListener("click", (e) => {
            e.stopPropagation();
            selectContinent(cont, !!onSelect);
        });
    });
}

function openMapModal() {
    if (!cachedMapSvg) return;
    const modal = document.getElementById("mapModal");
    const host = document.getElementById("mapModalSvgHost");
    if (!modal || !host) return;

    host.innerHTML = cachedMapSvg;
    bindMapPaths(host, true);
    highlightContinentOnMap(document.getElementById("continent").value);
    applyMapZoom();

    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    document.getElementById("mapModalTitle").textContent = t("mapModalTitle");
}

function closeMapModal() {
    const modal = document.getElementById("mapModal");
    if (!modal) return;
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    highlightContinentOnMap(document.getElementById("continent").value);
}

function initMapToolbar() {
    const fsBtn = document.getElementById("btnMapFullscreen");
    if (fsBtn) fsBtn.textContent = t("btnMapFullscreen");

    document.getElementById("btnMapFullscreen")?.addEventListener("click", (e) => {
        e.stopPropagation();
        openMapModal();
    });
    document.getElementById("btnMapZoomIn")?.addEventListener("click", (e) => {
        e.stopPropagation();
        changeMapZoom(MAP_ZOOM_STEP);
    });
    document.getElementById("btnMapZoomOut")?.addEventListener("click", (e) => {
        e.stopPropagation();
        changeMapZoom(-MAP_ZOOM_STEP);
    });
    document.getElementById("btnMapZoomReset")?.addEventListener("click", (e) => {
        e.stopPropagation();
        resetMapZoom();
    });

    document.getElementById("btnModalZoomIn")?.addEventListener("click", () =>
        changeMapZoom(MAP_ZOOM_STEP),
    );
    document.getElementById("btnModalZoomOut")?.addEventListener("click", () =>
        changeMapZoom(-MAP_ZOOM_STEP),
    );
    document.getElementById("btnModalZoomReset")?.addEventListener("click", resetMapZoom);
    document.getElementById("mapModalClose")?.addEventListener("click", closeMapModal);
    document.getElementById("mapModalBackdrop")?.addEventListener("click", closeMapModal);

    const viewport = document.getElementById("mapViewport");
    viewport?.addEventListener("dblclick", (e) => {
        if (e.target.closest(".continent-path")) return;
        openMapModal();
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") closeMapModal();
    });

    const onWheelZoom = (e) => {
        if (!e.ctrlKey && !e.metaKey) return;
        e.preventDefault();
        changeMapZoom(e.deltaY < 0 ? MAP_ZOOM_STEP : -MAP_ZOOM_STEP);
    };
    viewport?.addEventListener("wheel", onWheelZoom, { passive: false });
    document.getElementById("mapModalBody")?.addEventListener("wheel", onWheelZoom, {
        passive: false,
    });
}

function buildMapLegend() {
    const leg = document.getElementById("mapLegend");
    if (!leg) return;
    leg.innerHTML = "";
    for (const id of Object.keys(CONTINENT_INFO)) {
        const info = CONTINENT_INFO[id];
        const span = document.createElement("span");
        span.innerHTML = `<i style="background:${info.color}"></i>${info[currentLang === "zh" ? "zh" : "en"]}`;
        leg.appendChild(span);
    }
}

function styleContinentTabs() {
    document.querySelectorAll(".continent-tab").forEach((btn) => {
        const c = btn.dataset.continent;
        if (!CONTINENT_INFO[c]) return;
        const label = CONTINENT_INFO[c][currentLang === "zh" ? "zh" : "en"];
        btn.innerHTML = `<span class="dot" style="background:${CONTINENT_INFO[c].color}"></span>${label}`;
    });
}

function initMap() {
    const host = document.getElementById("mapSvgHost");
    if (!host || !cachedMapSvg) return;

    bindMapPaths(host, false);
    styleContinentTabs();
    buildMapLegend();
    document.querySelectorAll(".continent-tab").forEach((btn) => {
        btn.onclick = () => selectContinent(btn.dataset.continent, false);
    });
    highlightContinentOnMap(document.getElementById("continent").value);
    applyMapZoom();
}

async function loadWorldMap() {
    const host = document.getElementById("mapSvgHost");
    const loading = document.getElementById("mapLoading");
    if (!host) return;

    try {
        const res = await fetch("data/world-map.svg");
        if (!res.ok) throw new Error(String(res.status));
        cachedMapSvg = await res.text();
        host.innerHTML = cachedMapSvg;
        initMap();
        initMapToolbar();
    } catch (err) {
        console.error("world-map.svg load failed", err);
        host.innerHTML = `<p class="map-error">${currentLang === "zh" ? "地图加载失败，请通过 python3 serve.py 访问" : "Map failed to load. Use python3 serve.py"}</p>`;
    }
    if (loading) loading.remove();
}

function syncContinentTabs() {
    document.querySelectorAll(".continent-tab").forEach((btn) => {
        btn.classList.toggle("active", btn.dataset.continent === selectedContinent);
    });
}

/* —— Search —— */
function normalizeSearch(s) {
    return s.toLowerCase().replace(/\s+/g, "");
}

function fuzzyScore(query, target) {
    const q = normalizeSearch(query);
    const t = normalizeSearch(target);
    if (!q) return 0;
    if (t.includes(q)) return 100 - (t.length - q.length);
    let qi = 0;
    for (let i = 0; i < t.length && qi < q.length; i++) {
        if (t[i] === q[qi]) qi++;
    }
    if (qi === q.length) return 40 - q.length;
    return 0;
}

function buildSearchIndex() {
    searchIndex = [];
    const zh = currentLang === "zh";
    for (const prov in DATA) {
        for (const city in DATA[prov]) {
            const label = `中国 ${prov} ${city}`;
            const labelEn = `China ${prov} ${city}`;
            searchIndex.push({
                country: "china",
                prov,
                city,
                continent: "asia",
                text: label + " " + labelEn + " " + city + " " + prov,
            });
        }
    }
    for (const code in GLOBAL_DATA) {
        const c = GLOBAL_DATA[code];
        const cont = COUNTRY_CONTINENT[code];
        for (const prov in c.regions) {
            for (const city in c.regions[prov]) {
                searchIndex.push({
                    country: code,
                    prov,
                    city,
                    continent: cont,
                    text: `${c.name.zh} ${c.name.en} ${prov} ${city} ${c.code}`,
                });
            }
        }
    }
}

function renderSearchResults(items) {
    const box = document.getElementById("searchResults");
    box.innerHTML = "";
    if (!items.length) {
        box.innerHTML = `<div class="search-empty">${t("noSearch")}</div>`;
        box.classList.add("show");
        return;
    }
    items.slice(0, 12).forEach((item) => {
        const div = document.createElement("div");
        div.className = "search-item";
        const cName = getCountryName(item.country);
        div.textContent = `${cName} · ${item.prov} · ${item.city}`;
        div.addEventListener("click", () => applySearchSelection(item));
        box.appendChild(div);
    });
    box.classList.add("show");
}

function onSearchInput() {
    clearTimeout(searchTimer);
    const q = document.getElementById("searchInput").value.trim();
    const box = document.getElementById("searchResults");
    if (!q) {
        box.classList.remove("show");
        return;
    }
    searchTimer = setTimeout(() => {
        const scored = searchIndex
            .map((item) => ({ item, score: fuzzyScore(q, item.text) }))
            .filter((x) => x.score > 0)
            .sort((a, b) => b.score - a.score);
        renderSearchResults(scored.map((x) => x.item));
    }, 120);
}

function applySearchSelection(item) {
    document.getElementById("searchResults").classList.remove("show");
    document.getElementById("searchInput").value =
        `${getCountryName(item.country)} ${item.prov} ${item.city}`;
    if (item.continent) {
        document.getElementById("continent").value = item.continent;
        selectedContinent = item.continent;
        highlightContinentOnMap(item.continent);
        buildCountrySelect();
    }
    document.getElementById("country").value = item.country;
    updateRegions();
    document.getElementById("province").value = item.prov;
    updateCities();
    document.getElementById("city").value = item.city;
    calculate();
}

/* —— Calculate & AI —— */
function getAISuggest(country, city, w50, s50) {
    const txt = LANG[currentLang];
    let riskLevel = txt.riskLow;
    let riskClass = "risk-low";
    let suggest = "";
    if (COASTAL_CITIES.includes(city) || w50 >= 0.6) {
        riskLevel = txt.riskHigh;
        riskClass = "risk-high";
        suggest = txt.coastalWind;
    } else if (s50 >= 0.45) {
        riskLevel = txt.riskHigh;
        riskClass = "risk-high";
        suggest = txt.heavySnow;
    } else if (w50 >= 0.45 || s50 >= 0.35) {
        riskLevel = txt.riskMid;
        riskClass = "risk-mid";
        suggest = txt.midLoad;
    } else {
        suggest = txt.lowLoad;
    }
    if (country !== "china") {
        suggest += "\n" + txt.stdTip.replace("{std}", GLOBAL_DATA[country].standard[currentLang]);
    }
    suggest += "\n" + txt.conclusion.replace("{city}", city).replace("{risk}", riskLevel);
    return { riskLevel, riskClass, suggest };
}

function calculate() {
    const country = document.getElementById("country").value;
    const prov = document.getElementById("province").value;
    const city = document.getElementById("city").value;
    const period = document.getElementById("returnPeriod").value;
    const coeff = PERIOD_COEFF[period];
    const errDom = document.getElementById("error");
    const resDom = document.getElementById("result");

    errDom.classList.remove("show");
    resDom.classList.remove("show");

    if (!document.getElementById("continent").value) {
        errDom.innerText = t("errContinent");
        errDom.classList.add("show");
        return;
    }
    if (!prov) {
        errDom.innerText = t("errProvince");
        errDom.classList.add("show");
        return;
    }
    if (!city) {
        errDom.innerText = t("errCity");
        errDom.classList.add("show");
        return;
    }

    const loads = getLoadData(country, prov, city);
    if (!loads) {
        errDom.innerText = t("errNoData");
        errDom.classList.add("show");
        return;
    }
    const [w50, s50] = loads;
    const wCurVal = w50 * coeff;
    const sCurVal = s50 * coeff;

    document.getElementById("location").innerText =
        `${getCountryName(country)} · ${prov} · ${city}`;
    const codeRow = document.getElementById("codeRow");
    const codeStd = document.getElementById("codeStd");
    if (country === "china") {
        codeRow.style.display = "flex";
        codeStd.innerText = currentLang === "zh"
            ? "GB 50009-2012 附录E.5"
            : "GB 50009-2012 Appendix E.5";
    } else if (GLOBAL_DATA[country]) {
        codeRow.style.display = "flex";
        codeStd.innerText = GLOBAL_DATA[country].standard[currentLang];
    } else {
        codeRow.style.display = "none";
    }

    const pl = period + (currentLang === "zh" ? "年" : "yr");
    document.getElementById("textWindCur").innerText = `${pl} ${t("textWindCur")}`;
    document.getElementById("textSnowCur").innerText = `${pl} ${t("textSnowCur")}`;

    document.getElementById("wBase").innerText = w50.toFixed(2) + " kN/m²";
    document.getElementById("sBase").innerText = s50.toFixed(2) + " kN/m²";
    document.getElementById("wCur").innerText = wCurVal.toFixed(3) + " kN/m²";
    document.getElementById("sCur").innerText = sCurVal.toFixed(3) + " kN/m²";
    document.getElementById("w_pa").innerText = (wCurVal * KN_TO_PA).toFixed(2) + " Pa";
    document.getElementById("w_kgf").innerText = (wCurVal * KN_TO_KGF).toFixed(2) + " kgf/m²";
    document.getElementById("w_psf").innerText = (wCurVal * KN_TO_PSF).toFixed(2) + " psf";
    document.getElementById("s_pa").innerText = (sCurVal * KN_TO_PA).toFixed(2) + " Pa";
    document.getElementById("s_kgf").innerText = (sCurVal * KN_TO_KGF).toFixed(2) + " kgf/m²";
    document.getElementById("s_psf").innerText = (sCurVal * KN_TO_PSF).toFixed(2) + " psf";

    const aiRes = getAISuggest(country, city, w50, s50);
    document.getElementById("aiWrap").innerHTML = `
        <div class="ai-suggest">
            <div class="ai-title">${t("aiTitle")}</div>
            <span class="risk ${aiRes.riskClass}">${aiRes.riskLevel}</span>
            <div class="ai-body">${aiRes.suggest}</div>
        </div>`;
    resDom.classList.add("show");
    document.getElementById("resultPlaceholder").classList.add("hidden");
}

function applyLangToUI() {
    const ids = [
        "mainTitle", "subTitle", "labelContinent", "labelCountry", "labelPeriod",
        "labelProvince", "labelCity", "labelSearch", "btnCalc", "textCode",
        "textWind50", "textSnow50", "unitTitle", "textWPa", "textWKgf", "textWPsf",
        "textSPa", "textSKgf", "textSPsf", "noteText", "sourceText", "mapHint", "btnMapFullscreen",
    ];
    const keys = [
        "mainTitle", "subTitle", "labelContinent", "labelCountry", "labelPeriod",
        "labelProvince", "labelCity", "labelSearch", "btnCalc", "textCode",
        "textWind50", "textSnow50", "unitTitle", "textWPa", "textWKgf", "textWPsf",
        "textSPa", "textSKgf", "textSPsf", "noteText", "sourceText", "mapHint", "btnMapFullscreen",
    ];
    keys.forEach((k, i) => {
        const el = document.getElementById(ids[i]);
        if (el) el.textContent = t(k);
    });
    document.getElementById("searchInput").placeholder = t("searchPlaceholder");
    const ph = document.getElementById("resultPlaceholder");
    if (ph) ph.textContent = t("resultPlaceholder");
    styleContinentTabs();
    buildMapLegend();
    const mtitle = document.getElementById("mapModalTitle");
    if (mtitle && document.getElementById("mapModal")?.classList.contains("open"))
        mtitle.textContent = t("mapModalTitle");
}

function switchLang(lang) {
    currentLang = lang;
    document.getElementById("btnZh").classList.toggle("active", lang === "zh");
    document.getElementById("btnEn").classList.toggle("active", lang === "en");
    applyLangToUI();
    buildSearchIndex();
    buildContinentSelect();
    buildCountrySelect();
    updateRegions();
    updateCountTip();
    updatePeriodTip();
    styleContinentTabs();
    buildMapLegend();
    highlightContinentOnMap(document.getElementById("continent").value);
}

async function init() {
    buildSearchIndex();
    buildContinentSelect();
    buildCountrySelect();
    applyLangToUI();
    updateCountTip();
    updatePeriodTip();

    await loadWorldMap();

    document.getElementById("continent").addEventListener("change", () => onContinentChange(false));
    document.getElementById("country").addEventListener("change", onCountryChange);
    document.getElementById("province").addEventListener("change", updateCities);
    document.getElementById("returnPeriod").addEventListener("change", updatePeriodTip);
    document.getElementById("searchInput").addEventListener("input", onSearchInput);
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".search-wrap"))
            document.getElementById("searchResults").classList.remove("show");
    });
}

window.switchLang = switchLang;
window.calculate = calculate;
window.onload = init;

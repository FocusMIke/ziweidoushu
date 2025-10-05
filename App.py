# app.py
# -*- coding: utf-8 -*-
import datetime
import streamlit as st # 导入streamlit库

# =====================================================================================
# =============================== 用户配置区域 (CONFIG) ===============================
# =====================================================================================
# 核心数据定义 (这部分代码保持不变)
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
PALACE_NAMES = ["命宫", "兄弟宫", "夫妻宫", "子女宫", "财帛宫", "疾厄宫", "迁移宫", "仆役宫", "事业宫", "田宅宫", "福德宫", "父母宫"]
WU_XING_JU_NAMES = {2: "水二局", 3: "木三局", 4: "金四局", 5: "土五局", 6: "火六局"}
HUA_LU = {"甲": "廉贞", "乙": "天机", "丙": "天同", "丁": "太阴", "戊": "贪狼", "己": "武曲", "庚": "太阳", "辛": "巨门", "壬": "天梁", "癸": "破军"}
HUA_QUAN = {"甲": "破军", "乙": "天梁", "丙": "天机", "丁": "天同", "戊": "太阴", "己": "贪狼", "庚": "武曲", "辛": "太阳", "壬": "紫微", "癸": "巨门"}
HUA_KE = {"甲": "武曲", "乙": "紫微", "丙": "文昌", "丁": "天机", "戊": "右弼", "己": "天梁", "庚": "太阴", "辛": "文曲", "壬": "左辅", "癸": "太阴"}
HUA_JI = {"甲": "太阳", "乙": "太阴", "丙": "廉贞", "丁": "巨门", "戊": "天机", "己": "文曲", "庚": "天同", "辛": "文昌", "壬": "武曲", "癸": "贪狼"}
ZIWEI_GROUP = {"紫微": 0, "天机": -1, "太阳": -3, "武曲": -4, "天同": -5, "廉贞": -8}
TIANFU_GROUP = {"天府": 0, "太阴": 1, "贪狼": 2, "巨门": 3, "天相": 4, "天梁": 5, "七杀": 6, "破军": 10}

# NatalChart 类和 get_gan_of_date 函数 (这部分代码保持不变)
class NatalChart:
    def __init__(self, year, lunar_month, lunar_day, hour):
        self.star_pos_idx = {}
        self.palace_pos_idx = {}
        self.natal_hua_ji_idx = -1
        
        year_gan_idx = (year - 4) % 10
        year_gan = HEAVENLY_STEMS[year_gan_idx]
        
        self._calculate_chart(year_gan, lunar_month, lunar_day, hour)
        self.year_gan = year_gan

    def _calculate_chart(self, year_gan, lunar_month, lunar_day, hour):
        # ... (此处的代码与你提供的一模一样，为了简洁省略) ...
        hour_zhi_idx = (hour + 1) // 2 % 12 if hour != 23 else 0
        ming_gong_idx = (lunar_month - 1 - hour_zhi_idx + 12) % 12
        self.palace_pos_idx["命宫"] = ming_gong_idx
        for i in range(12):
            palace_idx = (ming_gong_idx - i + 12) % 12
            self.palace_pos_idx[PALACE_NAMES[i]] = palace_idx
        # ... (所有计算逻辑都保持原样) ...
        # 注意：省略了你代码中的大部分计算逻辑以保持这里的清晰度，实际使用时请完整复制
        ming_gong_ganzhi_stem_idx = ((HEAVENLY_STEMS.index(year_gan) % 5) * 2 + ming_gong_idx) % 10
        ming_gong_ganzhi = HEAVENLY_STEMS[ming_gong_ganzhi_stem_idx] + EARTHLY_BRANCHES[ming_gong_idx]
        ju_map = {
             "甲子":4, "乙丑":4, "丙寅":3, "丁卯":3, "戊辰":5, "己巳":5, "庚午":6, "辛未":6, "壬申":2, "癸酉":2, "甲戌":4, "乙亥":4,
             "丙子":2, "丁丑":2, "戊寅":6, "己卯":6, "庚辰":4, "辛巳":4, "壬午":5, "癸未":5, "甲申":3, "乙酉":3, "丙戌":6, "丁亥":6,
             "戊子":6, "己丑":6, "庚寅":5, "辛卯":5, "壬辰":2, "癸巳":2, "甲午":4, "乙未":4, "丙申":6, "丁酉":6, "戊戌":5, "己亥":5,
             "庚子":5, "辛丑":5, "壬寅":4, "癸卯":4, "甲辰":6, "乙巳":6, "丙午":2, "丁未":2, "戊申":5, "己酉":5, "庚戌":4, "辛亥":4,
             "壬子":3, "癸丑":3, "甲寅":2, "乙卯":2, "丙辰":5, "丁巳":5, "戊午":6, "己未":6, "庚申":3, "辛酉":3, "壬戌":2, "癸亥":2
        }
        wu_xing_ju = ju_map[ming_gong_ganzhi]
        shang, yushu = divmod(lunar_day, wu_xing_ju)
        if yushu == 0: shang -=1; yushu = wu_xing_ju
        temp_list = [1,0,3,2,5,4] # 寅 丑 辰 卯 午 巳
        temp = temp_list[ming_gong_idx % 6]
        ziwei_idx = (temp + (yushu-1) * (1 if ming_gong_idx in [2,3,4,5,6,7] else -1) + 12) % 12
        if shang % 2 != 0:
            ziwei_idx = (temp - (yushu-1) * (1 if ming_gong_idx in [2,3,4,5,6,7] else -1) + 12) % 12
        
        ziwei_idx = next( (i for i,x in enumerate([2,1,4,3,6,5]) if x == wu_xing_ju), 0)
        ziwei_idx = (ziwei_idx + (yushu - 1) * (1 if shang % 2 == 0 else -1) + 12) % 12

        for star, offset in ZIWEI_GROUP.items(): self.star_pos_idx[star] = (ziwei_idx + offset + 12) % 12
        tianfu_idx = (5 - ziwei_idx + 12) % 12
        for star, offset in TIANFU_GROUP.items(): self.star_pos_idx[star] = (tianfu_idx + offset) % 12
        self.star_pos_idx["左辅"], self.star_pos_idx["右弼"] = (lunar_month - 1 + 2) % 12, (11 - (lunar_month - 1)) % 12
        self.star_pos_idx["文昌"], self.star_pos_idx["文曲"] = (10 - hour_zhi_idx + 12) % 12, (4 + hour_zhi_idx) % 12
        natal_ji_star = HUA_JI.get(year_gan)
        self.natal_hua_ji_idx = self.star_pos_idx.get(natal_ji_star, -1)

    def _get_branch_name(self, index):
        return EARTHLY_BRANCHES[index] if 0 <= index < 12 else "未知"

    def analyze_day(self, daily_stem):
        # ... (这个函数也完全不变，省略) ...
        lu_star, quan_star, ke_star, ji_star = HUA_LU.get(daily_stem), HUA_QUAN.get(daily_stem), HUA_KE.get(daily_stem), HUA_JI.get(daily_stem)
        lu_pos_idx, quan_pos_idx, ke_pos_idx, ji_pos_idx = self.star_pos_idx.get(lu_star, -1), self.star_pos_idx.get(quan_star, -1), self.star_pos_idx.get(ke_star, -1), self.star_pos_idx.get(ji_star, -1)
        score, analysis_log = 0, []
        if lu_pos_idx != -1:
            if lu_pos_idx == self.palace_pos_idx.get("财帛宫"): score += 1; analysis_log.append(f"  • [吉+1] 流日化禄 ({lu_star}禄) 进入本命财帛宫 (在{self._get_branch_name(lu_pos_idx)}宫)，主今日有直接的财务机遇或进账。")
            if lu_pos_idx == self.palace_pos_idx.get("福德宫"): score += 1; analysis_log.append(f"  • [吉+1] 流日化禄 ({lu_star}禄) 进入本命福德宫 (在{self._get_branch_name(lu_pos_idx)}宫)，主今日心态愉悦，直觉敏锐，利于投机和决策。")
            if lu_pos_idx == self.palace_pos_idx.get("命宫"): score += 1; analysis_log.append(f"  • [吉+1] 流日化禄 ({lu_star}禄) 进入本命命宫 (在{self._get_branch_name(lu_pos_idx)}宫)，主今日整体运势顺遂，心情佳，人缘好。")
        if quan_pos_idx != -1 and (quan_pos_idx == self.palace_pos_idx.get("财帛宫") or quan_pos_idx == self.palace_pos_idx.get("命宫")): score += 1; analysis_log.append(f"  • [吉+1] 流日化权 ({quan_star}权) 进入关键宫位 (在{self._get_branch_name(quan_pos_idx)}宫)，主今日决策果断，掌控力强，利于主动出击。")
        if ji_pos_idx != -1:
            clashed_by_ji_idx = (ji_pos_idx + 6) % 12
            clashed_palace_name = self._get_branch_name(clashed_by_ji_idx)
            if clashed_by_ji_idx == self.natal_hua_ji_idx and self.natal_hua_ji_idx != -1:
                score = -2; analysis_log.append(f"  • [!!!最大风险!!!] 流日化忌 ({ji_star}忌) 在{self._get_branch_name(ji_pos_idx)}宫，猛烈冲击位于{clashed_palace_name}宫的生年化忌星。此为“冲起忌星”，是为大凶之兆，极易引爆命中固有隐患，应万事谨慎，规避风险！")
            else:
                if clashed_by_ji_idx == self.palace_pos_idx.get("财帛宫"): score -= 2; analysis_log.append(f"  • [大凶-2] 流日化忌 ({ji_star}忌) 直冲本命财帛宫 (在{clashed_palace_name}宫)，谨防因{self._get_branch_name(ji_pos_idx)}宫相关人事物引发的突然破财。")
                if clashed_by_ji_idx == self.palace_pos_idx.get("福德宫"): score -= 2; analysis_log.append(f"  • [大凶-2] 流日化忌 ({ji_star}忌) 直冲本命福德宫 (在{clashed_palace_name}宫)，心态极易失衡，判断力严重下降，绝不宜做任何投机决定。")
                if clashed_by_ji_idx == self.palace_pos_idx.get("命宫"): score -= 2; analysis_log.append(f"  • [大凶-2] 流日化忌 ({ji_star}忌) 直冲本命命宫 (在{clashed_palace_name}宫)，运势严重受阻，易感压力巨大，身心俱疲。")
            if ji_pos_idx == self.palace_pos_idx.get("财帛宫"): score -= 1; analysis_log.append(f"  • [凶-1] 流日化忌 ({ji_star}忌) 坐入本命财帛宫 (在{self._get_branch_name(ji_pos_idx)}宫)，主今日为财奔波烦恼，易有财务压力。")
            if ji_pos_idx == self.palace_pos_idx.get("福德宫"): score -= 1; analysis_log.append(f"  • [凶-1] 流日化忌 ({ji_star}忌) 坐入本命福德宫 (在{self._get_branch_name(ji_pos_idx)}宫)，主今日思绪混乱，内心不宁，易钻牛角尖。")
        
        final_score = max(-2, min(2, score))
        if not analysis_log: analysis_log.append("  • 今日无重大吉凶星象引动关键宫位，运势平稳。")
        
        interpretations = {2: "大吉", 1: "吉", 0: "平", -1: "凶", -2: "大凶"}
        interpretation_details = {2: "机会极佳，果断出击", 1: "运势顺利，可积极作为", 0: "无明显吉凶，宜静观其变", -1: "诸事不宜，谨慎防守", -2: "风险极高，规避为上"}

        return {
            "transformations": {"禄": f"{lu_star} ({self._get_branch_name(lu_pos_idx)})", "权": f"{quan_star} ({self._get_branch_name(quan_pos_idx)})", "科": f"{ke_star} ({self._get_branch_name(ke_pos_idx)})", "忌": f"{ji_star} ({self._get_branch_name(ji_pos_idx)})"},
            "score": final_score, "interpretation": interpretations.get(final_score), "interpretation_details": interpretation_details.get(final_score),
            "analysis_log": "\n".join(analysis_log)
        }

def get_gan_of_date(target_date):
    ref_date = datetime.date(2000, 1, 1)
    ref_gan_index = 6
    days_diff = (target_date - ref_date).days
    target_gan_index = (ref_gan_index + days_diff % 10 + 10) % 10
    return HEAVENLY_STEMS[target_gan_index]


# ===================================================================
# 执行与输出 (Streamlit 版本)
# ===================================================================
st.set_page_config(page_title="紫微斗数-每日偏财分析", layout="centered")
st.title("🔮 紫微斗数-每日偏财分析")
st.caption("v5.0 - Web App 版")

with st.sidebar:
    st.header("👤 您的出生信息")
    st.info("信息仅用于本次计算，不会被储存。")
    # 使用Streamlit的组件替换原来的固定变量
    birth_year = st.number_input("公历出生年份", min_value=1930, max_value=2023, value=2001, help="请输入4位公历年份")
    birth_lunar_month = st.selectbox("农历出生月份", options=list(range(1, 13)), index=1)
    birth_lunar_day = st.selectbox("农历出生日期", options=list(range(1, 31)), index=7)
    birth_hour = st.slider("出生时辰 (24小时制)", min_value=0, max_value=23, value=16)

st.header("📅 您要分析的日期")
target_date = st.date_input("选择日期", datetime.date(2025, 10, 8))

# 添加一个分析按钮
if st.button("开始分析"):
    try:
        # 1. 初始化命盘
        my_chart = NatalChart(birth_year, birth_lunar_month, birth_lunar_day, birth_hour)
        
        # 2. 自动计算目标日期的天干
        target_date_gan = get_gan_of_date(target_date)
        
        # 3. 使用自动计算出的天干进行分析
        daily_luck = my_chart.analyze_day(target_date_gan)

        st.subheader(f"📅 {target_date.strftime('%Y-%m-%d')} 分析报告")
        
        # 使用 st.metric 展示核心评级
        st.metric(label=f"综合评级: {daily_luck['interpretation']}", value=daily_luck['interpretation_details'], delta=f"分数: {daily_luck['score']}")
        
        with st.expander("【点击查看当日四化状态】"):
            cols = st.columns(4)
            hua_map = {"禄": "green", "权": "blue", "科": "orange", "忌": "red"}
            for i, (hua, star_info) in enumerate(daily_luck['transformations'].items()):
                with cols[i]:
                    st.markdown(f"**化{hua}**")
                    st.markdown(f"> <font color='{hua_map[hua]}'>{star_info}</font>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("【推演过程与建议】")
        st.info(daily_luck['analysis_log'])

    except Exception as e:
        st.error(f"发生错误：{e}")
        st.warning("请仔细检查您在左侧栏输入的生日信息是否正确。")

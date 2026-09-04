#!/usr/bin/env python3
"""Patch config/settings_data.json — padrão Veltrus C-level Saibai."""

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETTINGS_PATH = ROOT / "config" / "settings_data.json"

GREEN = "#76BD22"
GREEN_HOVER = "#5A9018"
GREEN_LIGHT = "#E8F5D4"
BG_LIGHT = "#F4F9F0"
BG_WHITE = "#FFFFFF"
BG_OFF = "#FAFDF7"
DARK = "#2A3A1A"
TEXT = "#4E6040"
TERRA = "#3D2B1F"
BORDER = "#E2EDDA"
SHADOW = "#00000015"

BASE = {
    "background_gradient": "",
    "primary": GREEN,
    "primary_hover": GREEN_HOVER,
    "border": BORDER,
    "shadow": SHADOW,
    "primary_button_background": GREEN,
    "primary_button_background_gradient": "",
    "primary_button_text": "#FFFFFF",
    "primary_button_border": GREEN,
    "primary_button_hover_background": GREEN_HOVER,
    "primary_button_hover_background_gradient": "",
    "primary_button_hover_text": "#FFFFFF",
    "primary_button_hover_border": GREEN_HOVER,
    "secondary_button_background": "rgba(0,0,0,0)",
    "secondary_button_background_gradient": "",
    "secondary_button_text": GREEN,
    "secondary_button_border": GREEN,
    "secondary_button_hover_background": GREEN,
    "secondary_button_hover_background_gradient": "",
    "secondary_button_hover_text": "#FFFFFF",
    "secondary_button_hover_border": GREEN,
    "input_background": BG_WHITE,
    "input_text_color": DARK,
    "input_border_color": "#C5DBA8",
    "input_hover_background": GREEN_LIGHT,
    "arrow_color": GREEN,
    "arrow_background": "rgba(0,0,0,0)",
    "arrow_border": "rgba(0,0,0,0)",
    "arrow_color_hover": GREEN_HOVER,
    "arrow_background_hover": GREEN_LIGHT,
    "pagination_color": TEXT,
    "pagination_active_color": GREEN,
}

SCHEME_VARIANTS = {
    "scheme-1": {"background": BG_WHITE, "foreground_heading": DARK, "foreground": TEXT},
    "scheme-2": {"background": BG_LIGHT, "foreground_heading": DARK, "foreground": TEXT},
    "scheme-3": {"background": GREEN_LIGHT, "foreground_heading": DARK, "foreground": TEXT},
    "scheme-4": {
        "background": GREEN,
        "foreground_heading": "#FFFFFF",
        "foreground": "#FFFFFF",
        "primary": "#FFFFFF",
        "primary_hover": GREEN_LIGHT,
        "secondary_button_text": "#FFFFFF",
        "secondary_button_border": "#FFFFFF",
        "secondary_button_hover_background": "#FFFFFF",
        "secondary_button_hover_text": GREEN,
        "secondary_button_hover_border": "#FFFFFF",
    },
    "scheme-5": {
        "background": DARK,
        "foreground_heading": "#FFFFFF",
        "foreground": "#D4E4C8",
        "primary": GREEN,
        "primary_hover": GREEN_HOVER,
        "input_background": "rgba(255,255,255,0.08)",
        "input_text_color": "#FFFFFF",
        "input_border_color": "rgba(255,255,255,0.2)",
        "input_hover_background": "rgba(255,255,255,0.12)",
        "arrow_color": "#FFFFFF",
        "arrow_color_hover": GREEN,
        "pagination_color": "#D4E4C8",
    },
    "scheme-6": {
        "background": BG_WHITE,
        "foreground_heading": DARK,
        "foreground": TEXT,
        "primary": TERRA,
        "primary_hover": "#8B5E4A",
        "primary_button_background": TERRA,
        "primary_button_border": TERRA,
        "primary_button_hover_background": "#8B5E4A",
        "primary_button_hover_border": "#8B5E4A",
    },
    "scheme-7": {"background": BG_LIGHT, "foreground_heading": DARK, "foreground": TEXT},
    "scheme-8": {"background": BG_OFF, "foreground_heading": DARK, "foreground": TEXT},
    "scheme-9": {
        "background": "rgba(0,0,0,0)",
        "foreground_heading": "#FFFFFF",
        "foreground": "#FFFFFF",
        "primary": GREEN,
        "primary_hover": GREEN_HOVER,
        "border": "rgba(255,255,255,0.25)",
    },
    "scheme-10": {
        "background": DARK,
        "foreground_heading": "#FFFFFF",
        "foreground": "#B8C9A8",
        "primary": "#A8D56A",
        "primary_hover": GREEN,
    },
    "scheme-11": {"background": BG_WHITE, "foreground_heading": DARK, "foreground": TEXT},
    "scheme-12": {"background": BG_LIGHT, "foreground_heading": DARK, "foreground": TEXT},
    "scheme-13": {"background": GREEN_LIGHT, "foreground_heading": DARK, "foreground": TEXT},
}


def build_scheme(sid: str) -> dict:
    settings = deepcopy(BASE)
    settings.update(SCHEME_VARIANTS.get(sid, SCHEME_VARIANTS["scheme-1"]))
    return {"settings": settings}


def main() -> None:
    raw = SETTINGS_PATH.read_text(encoding="utf-8")
    header, _, body = raw.partition("{")
    data = json.loads("{" + body)
    cur = data["current"]

    # ── Logo e favicon ──
    cur["logo"] = ""
    cur["logo_inverse"] = ""
    cur["logo_width"] = 160
    cur["logo_width_mobile"] = 110

    # ── Tipografia (100% Jost, LP) ──
    cur["type_body_font"] = "jost_n4"
    cur["type_header_font"] = "jost_n4"
    cur["type_subheading_font"] = "jost_n4"
    cur["type_text_transform_h1"] = "none"
    cur["type_text_transform_h2"] = "none"
    cur["type_text_transform_h3"] = "none"
    cur["type_size_paragraph"] = "1.6rem"
    cur["type_line_height_paragraph"] = "body-normal"
    cur["type_font_h1"] = "heading"
    cur["type_size_h1"] = "4.0rem"
    cur["type_line_height_h1"] = "display-normal"
    cur["type_letter_spacing_h1"] = "heading-normal"
    cur["type_font_h2"] = "heading"
    cur["type_size_h2"] = "3.0rem"
    cur["type_font_h3"] = "heading"
    cur["type_size_h3"] = "2.4rem"

    # ── Layout ──
    cur["page_width"] = 1320
    cur["spacing_sections"] = 0
    cur["spacing_grid_horizontal"] = 24
    cur["spacing_grid_vertical"] = 24
    cur["enable_rtl_layout"] = False

    # ── Features (desligar demo Ella) ──
    cur["show_countdown"] = False
    cur["enable_multi_tab_layout_mobile"] = False
    cur["show_wishlist"] = False
    cur["enable_wishlist"] = False
    cur["show_hot_stock"] = False
    cur["show_dynamic_browser_title"] = False
    cur["show_floating_icons"] = False

    # ── Animações (sutil / performance) ──
    cur["animations_reveal_on_scroll"] = False
    cur["animations_hover_elements"] = "none"
    cur["enable_smooth_scroll"] = False
    cur["enable_preloading_screen"] = False

    # ── Botões ──
    cur["primary_button_border_width"] = 0
    cur["button_border_radius_primary"] = 4
    cur["button_border_radius_secondary"] = 4
    cur["button_type_font_primary"] = "body"
    cur["button_type_font_secondary"] = "body"
    cur["button_font_weight_primary"] = "500"
    cur["button_text_case_primary"] = "default"
    cur["button_text_case_secondary"] = "default"
    cur["buttons_border_thickness"] = 1
    cur["buttons_border_opacity"] = 100
    cur["buttons_radius"] = 4
    cur["buttons_shadow_opacity"] = 0
    cur["buttons_shadow_horizontal_offset"] = 0
    cur["buttons_shadow_vertical_offset"] = 0
    cur["buttons_shadow_blur"] = 0
    cur["buttons_padding_vertical"] = 14
    cur["buttons_padding_vertical_mobile"] = 12
    cur["buttons_padding_horizontal"] = 28
    cur["buttons_padding_horizontal_mobile"] = 20

    # ── Entradas ──
    cur["inputs_border_thickness"] = 1
    cur["inputs_border_opacity"] = 100
    cur["inputs_radius"] = 4
    cur["inputs_shadow_opacity"] = 0

    # ── Setas ──
    cur["arrows_type"] = "arrows_long"
    cur["arrows_width"] = 48
    cur["arrows_height"] = 28
    cur["arrows_icon_size"] = 32

    # ── Selos ──
    cur["badge_position"] = "custom"
    cur["badge_top"] = 12
    cur["badge_left"] = 12
    cur["badge_corner_radius"] = 2
    cur["badge_text_transform"] = "uppercase"
    cur["sale_badge_color"] = "#FFFFFF"
    cur["sale_badge_background"] = GREEN
    cur["sale_badge_color_scheme"] = "scheme-4"
    cur["sold_out_badge_color_scheme"] = "scheme-10"
    cur["show_new_badge"] = False
    cur["show_custom_badge"] = False
    cur["show_price_percent"] = True
    cur["enable_price_percent"] = True

    # ── Carrinho ──
    cur["cart_type"] = "drawer"
    cur["cart_color_scheme"] = "scheme-1"
    cur["cart_drawer_collection"] = "todos"
    cur["show_vendor"] = False
    cur["show_cart_note"] = True
    cur["show_cart_estimate_shipping"] = True
    cur["show_cart_coupon"] = True
    cur["gift_wrap_product"] = ""
    cur["show_quick_edit_cart"] = False
    cur["show_calculator_free_shipping_message"] = True
    cur["calculator_free_shipping_message_price"] = "320"

    # ── Cartões de produto ──
    cur["card_style"] = "standard"
    cur["card_color_scheme"] = "scheme-1"
    cur["card_text_alignment"] = "left"
    cur["card_image_padding"] = 0
    cur["card_border_thickness"] = 0
    cur["card_corner_radius"] = 0
    cur["card_shadow_opacity"] = 0
    cur["card_shadow_vertical_offset"] = 0
    cur["enable_wishlist"] = False
    cur["enable_quick_view"] = False
    cur["enable_compare"] = False
    cur["enable_price_wishlist"] = False
    cur["enable_price_compare"] = False
    cur["show_product_marquee"] = False
    cur["quick_add_type"] = "button"
    cur["swatch_type"] = "color"
    cur["variant_swatch_size"] = 22
    cur["variant_pills_radius"] = 4
    cur["variant_pills_border_thickness"] = 1
    cur["variant_pills_border_opacity"] = 100
    cur["variant_pills_shadow_opacity"] = 0

    # ── Coleção / blog cards ──
    cur["collection_card_style"] = "card"
    cur["collection_card_color_scheme"] = "scheme-2"
    cur["collection_card_corner_radius"] = 0
    cur["collection_card_shadow_opacity"] = 0
    cur["blog_card_color_scheme"] = "scheme-2"
    cur["blog_card_corner_radius"] = 0
    cur["blog_card_shadow_opacity"] = 0

    # ── Popovers / modais / media ──
    cur["popover_color_scheme"] = "scheme-1"
    cur["popover_drop_shadow"] = False
    cur["popover_border_width"] = 1
    cur["popover_border_radius"] = 4
    cur["text_boxes_border_thickness"] = 0
    cur["text_boxes_radius"] = 0
    cur["text_boxes_shadow_opacity"] = 0
    cur["media_border_thickness"] = 0
    cur["media_radius"] = 0
    cur["media_shadow_opacity"] = 0
    cur["drawer_shadow_opacity"] = 0
    cur["popup_shadow_opacity"] = 0

    # ── Busca ──
    cur["predictive_search_enabled"] = True
    cur["predictive_search_show_vendor"] = False
    cur["predictive_search_show_price"] = True

    # ── Moeda ──
    cur["currency_code_enabled"] = False

    # ── Redes sociais ──
    cur["social_instagram_link"] = "https://www.instagram.com/saibaisaladas/"
    cur["social_facebook_link"] = "https://www.facebook.com/saladas.saibai"
    cur["social_youtube_link"] = ""
    cur["social_tiktok_link"] = ""
    cur["social_pinterest_link"] = ""
    cur["social_twitter_link"] = ""
    cur["social_snapchat_link"] = ""
    cur["social_tumblr_link"] = ""
    cur["social_vimeo_link"] = ""

    # ── Categoria multinível ──
    cur["category_filter"] = ""
    cur["category_filter_label1"] = "Categoria"
    cur["category_filter_label2"] = "Subcategoria"
    cur["category_filter_label3"] = "Tipo"
    cur["color_filter_label"] = DARK
    cur["bg_filter_label"] = BG_WHITE
    cur["category_filter_button"] = "Buscar"
    cur["text_button_filter_color"] = "#FFFFFF"
    cur["bg_button_filter_color"] = GREEN
    cur["border_button_filter_color"] = GREEN
    cur["text_button_filter_color_hover"] = "#FFFFFF"
    cur["bg_button_filter_color_hover"] = GREEN_HOVER

    # ── Tracking: manter vazio — GA4/Meta vêm dos canais Shopify (anti-duplicata) ──
    cur["meta_pixel_id"] = ""
    cur["ga4_measurement_id"] = ""

    # ── Color schemes ──
    for sid in cur.get("color_schemes", {}):
        cur["color_schemes"][sid] = build_scheme(sid)

    out = header + json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    SETTINGS_PATH.write_text(out, encoding="utf-8")
    print(f"✓ Patched {SETTINGS_PATH}")


if __name__ == "__main__":
    main()

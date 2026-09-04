# Shopify Support — IndexController page_cache purge

**Store:** byinbz-0k.myshopify.com  
**Domain:** https://emporiosaibai.com.br  
**Live theme:** ella-saibai-homepage (#186796147006)  
**Partner / agency:** Veltrus (Shopify Partner)  
**Contact:** contato@saibai.com.br  

## Subject
Urgent: IndexController page_cache serving deleted theme HTML on homepage (no header)

## Request
Please purge the **Online Store IndexController page_cache** for this shop’s homepage (`/` on both `emporiosaibai.com.br` and `byinbz-0k.myshopify.com`).

## Evidence
1. `server-timing` correctly reports live theme `theme;desc="186796147006"`.
2. Anonymous HTML body still embeds:
   `Shopify.theme = {"name":"ella-saibai-homepage","id":186124239166,...}`
3. Theme `#186124239166` was **deleted** via Theme CLI; body still references it.
4. Response size stuck at **333912** bytes; ETag changes (`page_cache:92381937982:IndexController:*`) but body does not include current layout/header.
5. Preview with `?preview_theme_id=186796147006` returns correct HTML (~271k) with header (`data-saibai-header`, `saibai-build` meta).
6. `/search` serves the new theme correctly; only homepage (and some other cached templates) remain stale.

## Already attempted (no effect on anonymous `/`)
- `shopify theme push` / `themeFilesUpsert`
- `shopify theme publish` (new theme IDs)
- Theme rename, product tag update, menuUpdate
- Delete of old theme `#186124239166`
- index.json section ID changes

## Desired outcome
Anonymous GET `https://emporiosaibai.com.br/` must SSR the live theme layout including the Saibai header (nav: Produtos / Sobre / Contato / Receitas), matching preview.

## Priority
High — SEO/Googlebot and logged-out users currently receive homepage without site navigation.

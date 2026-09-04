#!/usr/bin/env python3
"""Otimização 10/10 — produtos ativos Empório Saibai (descrição, SEO, metafields, variantes)."""

import json
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional

STORE = "byinbz-0k.myshopify.com"
VENDOR = "Empório Saibai"
GOOGLE_CAT = "5798"

# Metaobjects Shopify
MO = {
    "food_outro": "gid://shopify/Metaobject/112745677118",
    "vegano": "gid://shopify/Metaobject/158246502718",
    "vegetariano": "gid://shopify/Metaobject/158246437182",
    "sem_gluten": "gid://shopify/Metaobject/158246568254",
    "origem_unica": "gid://shopify/Metaobject/161446560062",
    "sem_acucar": "gid://shopify/Metaobject/161446592830",
    "sem_lactose": "gid://shopify/Metaobject/161446527294",
    "baixo_sodio": "gid://shopify/Metaobject/161446330686",
    "no_preservatives": "gid://shopify/Metaobject/195075866942",
}

FOOD_DIET = [
    MO["vegano"], MO["vegetariano"], MO["sem_gluten"],
    MO["origem_unica"], MO["sem_lactose"], MO["baixo_sodio"], MO["no_preservatives"],
]
FRUIT_DIET = [
    MO["vegano"], MO["vegetariano"], MO["sem_gluten"],
    MO["origem_unica"], MO["sem_acucar"], MO["no_preservatives"],
]

SAIBAI_FOOTER = (
    "<hr><p><strong>Por que Empório Saibai?</strong></p>"
    "<ul>"
    "<li><strong>Produção própria:</strong> Do plantio à colheita em Piedade, interior de São Paulo.</li>"
    "<li><strong>Sem atravessadores:</strong> Controle total de qualidade, do campo à sua mesa.</li>"
    "<li><strong>Artesanal de verdade:</strong> Processos cuidadosos que preservam sabor, textura e procedência.</li>"
    "</ul>"
)

CONSERVAS = [
    "gid://shopify/Product/12367495201086",
    "gid://shopify/Product/12367495266622",
    "gid://shopify/Product/12367495528766",
]
FRUTAS = [
    "gid://shopify/Product/12367499329854",
    "gid://shopify/Product/12367499493694",
    "gid://shopify/Product/12367499886910",
    "gid://shopify/Product/12367500050750",
    "gid://shopify/Product/12367500214590",
]

PRODUCTS: List[Dict[str, Any]] = [
    {
        "id": "gid://shopify/Product/12367495201086",
        "title": "Conserva de Alcachofras - Fundo Inteiro",
        "productType": "Conservas",
        "tags": ["alcachofra", "conserva", "conservados", "gourmet", "artesanal", "piedade"],
        "seo": {
            "title": "Fundo Inteiro de Alcachofra em Conserva | Empório Saibai",
            "description": "Fundo inteiro de alcachofra artesanal em conserva. O filé mignon da horta, firme e carnoso. Tamanhos M e G. Produção própria Saibai, Piedade/SP.",
        },
        "summary": "Fundo inteiro de alcachofra em conserva artesanal. Peça carnosa e íntegra, ideal para entradas gourmet. Produção própria Saibai, Piedade/SP.",
        "search_queries": ["alcachofra conserva", "fundo alcachofra", "conserva gourmet", "empório saibai", "alcachofra artesanal"],
        "related": [CONSERVAS[1], CONSERVAS[2]],
        "complementary": [CONSERVAS[2]],
        "diet": FOOD_DIET,
        "food_taxonomy": True,
        "descriptionHtml": (
            "<p><strong>Fundo Inteiro de Alcachofra Saibai</strong> — o filé mignon da horta, cultivado e conservado na nossa fazenda em Piedade/SP.</p>"
            "<p>Selecionamos apenas as bases mais carnosas e íntegras da alcachofra (<em>Cynara scolymus</em>), garantindo peças firmes e macias que preservam a elegância natural desta iguaria mediterrânea. Cada fundo é cuidadosamente limpo e conservado para manter sabor terroso e textura aveludada.</p>"
            "<ul>"
            "<li><strong>Destaque visual:</strong> Peças inteiras e uniformes, ideais para entradas de luxo.</li>"
            "<li><strong>Textura carnuda:</strong> Absorve temperos e molhos com perfeição.</li>"
            "<li><strong>Pronto para servir:</strong> Abra, escorra e eleve qualquer prato em segundos.</li>"
            "</ul>"
            "<hr><p><strong>Sugestões de uso</strong></p>"
            "<ul>"
            "<li>Antepasto com azeite extra virgem, alho confitado e ervas finas.</li>"
            "<li>Base para risotos, massas artesanais e saladas premium.</li>"
            "<li>Entrada quente gratinada com queijo de cabra e tomilho.</li>"
            "</ul>"
            "<hr><p><strong>Ficha técnica</strong></p>"
            "<ul>"
            "<li><strong>Conteúdo líquido:</strong> M — aprox. 400 g | G — aprox. 700 g</li>"
            "<li><strong>Validade:</strong> 12 meses a partir da fabricação</li>"
            "<li><strong>Conservação:</strong> Local seco e ao abrigo da luz. Após aberto, refrigerar e consumir em até 3 dias</li>"
            "<li><strong>Ingredientes:</strong> Fundo de alcachofra, água, sal e acidulante ácido cítrico</li>"
            "<li>Sem conservantes artificiais · Vegano · Sem glúten · Produção própria · Piedade/SP</li>"
            "</ul>"
            + SAIBAI_FOOTER
        ),
        "variants": [
            {"id": "gid://shopify/ProductVariant/53412743446846", "weight": 400},
            {"id": "gid://shopify/ProductVariant/53412743479614", "weight": 700},
        ],
    },
    {
        "id": "gid://shopify/Product/12367495266622",
        "title": "Conserva de Alcachofras - Fundo Pedaço",
        "productType": "Conservas",
        "tags": ["alcachofra", "conserva", "conservados", "gourmet", "artesanal", "piedade"],
        "seo": {
            "title": "Fundo de Alcachofra em Pedaços em Conserva | Empório Saibai",
            "description": "Fundo de alcachofra em pedaços, conserva artesanal Saibai. Ingrediente ideal para receitas gourmet. Tamanhos M e G. Produção própria, Piedade/SP.",
        },
        "summary": "Fundo de alcachofra em pedaços em conserva artesanal. Textura densa e versátil para antepastos e receitas gourmet. Saibai, Piedade/SP.",
        "search_queries": ["alcachofra pedaços", "conserva alcachofra", "antepasto gourmet", "empório saibai"],
        "related": [CONSERVAS[0], CONSERVAS[2]],
        "complementary": [CONSERVAS[0]],
        "diet": FOOD_DIET,
        "food_taxonomy": True,
        "descriptionHtml": (
            "<p><strong>Fundo de Alcachofra Saibai em Pedaços</strong> — o ingrediente secreto dos chefs para entradas memoráveis, direto da nossa produção em Piedade/SP.</p>"
            "<p>A parte mais carnuda e íntegra da alcachofra, com textura densa e macia que se mantém firme após o preparo. Limpos e conservados para preservar o sabor terroso original — ideal para pratos recheados, antepastos e receitas onde o produto se integra ao molho.</p>"
            "<ul>"
            "<li><strong>A nobreza do fundo:</strong> Sem folhas, no ponto certo de conserva.</li>"
            "<li><strong>Pronto para criar:</strong> Recheios, gratinados e antepastos sofisticados.</li>"
            "<li><strong>Formato versátil:</strong> Pedaços irregulares que absorvem temperos com maestria.</li>"
            "</ul>"
            "<hr><p><strong>Sugestões de uso</strong></p>"
            "<ul>"
            "<li>Rechear com queijos cremosos, cogumelos ou servir gratinado.</li>"
            "<li>Antepasto mediterrâneo com azeite, limão e pimenta-do-reino.</li>"
            "<li>Saladas autorais, bruschettas e tábuas de frios premium.</li>"
            "</ul>"
            "<hr><p><strong>Ficha técnica</strong></p>"
            "<ul>"
            "<li><strong>Conteúdo líquido:</strong> M — aprox. 380 g | G — aprox. 650 g</li>"
            "<li><strong>Validade:</strong> 12 meses a partir da fabricação</li>"
            "<li><strong>Conservação:</strong> Local seco e ao abrigo da luz. Após aberto, refrigerar e consumir em até 3 dias</li>"
            "<li><strong>Ingredientes:</strong> Fundo de alcachofra em pedaços, água, sal e acidulante ácido cítrico</li>"
            "<li>Sem conservantes artificiais · Vegano · Sem glúten · Produção própria · Piedade/SP</li>"
            "</ul>"
            + SAIBAI_FOOTER
        ),
        "variants": [
            {"id": "gid://shopify/ProductVariant/53412743643454", "weight": 380},
            {"id": "gid://shopify/ProductVariant/53412743676222", "weight": 650},
        ],
    },
    {
        "id": "gid://shopify/Product/12367495528766",
        "title": "Conserva de Alcachofras - Coração",
        "productType": "Conservas",
        "tags": ["alcachofra", "conserva", "conservados", "gourmet", "artesanal", "piedade"],
        "seo": {
            "title": "Coração de Alcachofra em Conserva | Empório Saibai",
            "description": "Coração de alcachofra em conserva artesanal, a parte mais tenra e nobre. Tamanhos P, M e G. Direto do campo ao prato. Empório Saibai, Piedade/SP.",
        },
        "summary": "Coração de alcachofra em conserva — a parte mais tenra e nobre. Textura aveludada, sabor delicado. Três tamanhos. Empório Saibai, Piedade/SP.",
        "search_queries": ["coração alcachofra", "conserva alcachofra", "alcachofra tenra", "empório saibai"],
        "related": [CONSERVAS[0], CONSERVAS[1]],
        "complementary": [CONSERVAS[0], CONSERVAS[1]],
        "diet": FOOD_DIET,
        "food_taxonomy": True,
        "descriptionHtml": (
            "<p><strong>Coração de Alcachofra Saibai</strong> — a expressão máxima da sofisticação prática, cultivado e conservado na nossa fazenda em Piedade/SP.</p>"
            "<p>Selecionamos apenas a parte mais tenra e nobre da alcachofra (<em>Cynara scolymus</em>), criando uma conserva que equilibra frescor, textura aveludada e sabor delicadamente acidulado. Cada coração chega à sua mesa com integridade preservada — pronto para elevar qualquer receita.</p>"
            "<ul>"
            "<li><strong>Textura incomparável:</strong> Corações macios que derretem na boca.</li>"
            "<li><strong>Versatilidade gourmet:</strong> Antepastos, risotos, massas e saladas verdes.</li>"
            "<li><strong>Três tamanhos:</strong> P para uso imediato, M para jantares, G para eventos.</li>"
            "</ul>"
            "<hr><p><strong>Sugestões de uso</strong></p>"
            "<ul>"
            "<li>Antepasto com azeite trufado e parmesão ralado na hora.</li>"
            "<li>Risoto de coração de alcachofra com limão siciliano.</li>"
            "<li>Salada mediterrânea com rúcula, tomate cereja e balsâmico.</li>"
            "</ul>"
            "<hr><p><strong>Ficha técnica</strong></p>"
            "<ul>"
            "<li><strong>Conteúdo líquido:</strong> P — aprox. 180 g | M — aprox. 330 g | G — aprox. 550 g</li>"
            "<li><strong>Validade:</strong> 12 meses a partir da fabricação</li>"
            "<li><strong>Conservação:</strong> Local seco e ao abrigo da luz. Após aberto, refrigerar e consumir em até 3 dias</li>"
            "<li><strong>Ingredientes:</strong> Coração de alcachofra, água, sal e acidulante ácido cítrico</li>"
            "<li>Sem conservantes artificiais · Vegano · Sem glúten · Produção própria · Piedade/SP</li>"
            "</ul>"
            + SAIBAI_FOOTER
        ),
        "variants": [
            {"id": "gid://shopify/ProductVariant/53412760518974", "weight": 180},
            {"id": "gid://shopify/ProductVariant/53412744921406", "weight": 330},
            {"id": "gid://shopify/ProductVariant/53412744954174", "weight": 550},
        ],
    },
    {
        "id": "gid://shopify/Product/12367498772798",
        "title": "Flores Desidratadas",
        "productType": "Flores Desidratadas",
        "tags": ["flores", "desidratados", "decoracao", "gastronomia", "comestivel", "piedade"],
        "seo": {
            "title": "Flores Desidratadas Selecionadas | Empório Saibai",
            "description": "Flores desidratadas para decoração e gastronomia. Eleve o visual das suas criações com delicadeza e sofisticação. Empório Saibai, Piedade/SP.",
        },
        "summary": "Mix de flores comestíveis desidratadas para gastronomia e decoração. Cores vibrantes, 100% natural. Empório Saibai, Piedade/SP.",
        "search_queries": ["flores desidratadas", "flores comestíveis", "decoração gastronômica", "empório saibai"],
        "related": FRUTAS[:2],
        "complementary": FRUTAS,
        "diet": FRUIT_DIET,
        "remove_from_collection": None,
        "descriptionHtml": (
            "<p><strong>Flores Desidratadas Selecionadas Saibai</strong> — o detalhe que transforma pratos e drinks em obras de arte, cultivadas com rigor em Piedade/SP.</p>"
            "<p>Mais do que decoração, são o segredo de chefs e mixologistas para finalizações impecáveis. Processo de desidratação cuidadoso que preserva cores vibrantes e formas naturais por muito mais tempo que flores frescas.</p>"
            "<ul>"
            "<li><strong>Beleza duradoura:</strong> Mantém estética por semanas em ambiente seco.</li>"
            "<li><strong>Versatilidade gourmet:</strong> Coquetéis, sobremesas, risotos e saladas autorais.</li>"
            "<li><strong>100% natural:</strong> Sem aditivos — a primeira mordida é com os olhos.</li>"
            "</ul>"
            "<hr><p><strong>Sugestões de uso</strong></p>"
            "<ul>"
            "<li>Guarnição de coquetéis, gin tônica e drinques autorais.</li>"
            "<li>Decoração de sobremesas, bolos naked e mesas de eventos.</li>"
            "<li>Finalização de risotos, saladas e pratos de alta gastronomia.</li>"
            "</ul>"
            "<hr><p><strong>Ficha técnica</strong></p>"
            "<ul>"
            "<li><strong>Conteúdo:</strong> Aprox. 15 g (mix variado conforme safra)</li>"
            "<li><strong>Validade:</strong> 12 meses em embalagem fechada</li>"
            "<li><strong>Conservação:</strong> Local fresco, seco, ao abrigo de umidade e luz direta</li>"
            "<li><strong>Ingredientes:</strong> Mix de flores comestíveis desidratadas (espécies variadas conforme safra)</li>"
            "<li>Sem conservantes · Natural · Vegano · Produção artesanal · Piedade/SP</li>"
            "</ul>"
            + SAIBAI_FOOTER
        ),
        "variants": [{"id": "gid://shopify/ProductVariant/53412766712126", "weight": 15}],
    },
    {
        "id": "gid://shopify/Product/12367499329854",
        "title": "Frutas Desidratadas - Doce Pomar 200g",
        "productType": "Frutas Desidratadas",
        "tags": ["frutas", "desidratados", "snack", "natural", "doce pomar", "piedade"],
        "seo": {
            "title": "Frutas Desidratadas Doce Pomar 200g | Empório Saibai",
            "description": "Mix Doce Pomar com frutas desidratadas selecionadas. Energia natural, sabor intenso e zero aditivos. 200g. Empório Saibai, Piedade/SP.",
        },
        "summary": "Mix Doce Pomar — frutas desidratadas selecionadas, 200g. Snack natural sem açúcar adicionado. Empório Saibai, Piedade/SP.",
        "search_queries": ["frutas desidratadas", "snack natural", "doce pomar", "frutas secas", "empório saibai"],
        "related": FRUTAS[1:],
        "complementary": CONSERVAS,
        "diet": FRUIT_DIET,
        "descriptionHtml": (
            "<p><strong>Mix Doce Pomar Saibai</strong> — redescubra o sabor da fruta em sua forma mais intensa, 200g de energia natural cultivada em Piedade/SP.</p>"
            "<p>Seleção rigorosa de frutas desidratadas para quem exige qualidade gourmet em cada mordida. Processo cuidadoso que remove a água e preserva fibras, vitaminas e açúcar natural — snack leve, nutritivo e irresistível.</p>"
            "<ul>"
            "<li><strong>Lanche inteligente:</strong> Bolsa, escritório ou lanche escolar.</li>"
            "<li><strong>Versatilidade:</strong> Iogurte, granola, saladas e sobremesas.</li>"
            "<li><strong>Doçura natural:</strong> Frutas no auge da maturação, zero aditivos.</li>"
            "</ul>"
            "<hr><p><strong>Sugestões de uso</strong></p>"
            "<ul>"
            "<li>Snack energético pré ou pós-treino.</li>"
            "<li>Acrescentar a bowls de açaí, iogurte grego ou overnight oats.</li>"
            "<li>Finalização de sobremesas, panetones artesanais e tábuas de queijos.</li>"
            "</ul>"
            "<hr><p><strong>Ficha técnica</strong></p>"
            "<ul>"
            "<li><strong>Peso líquido:</strong> 200 g</li>"
            "<li><strong>Validade:</strong> 12 meses em embalagem fechada</li>"
            "<li><strong>Conservação:</strong> Local fresco, seco e ao abrigo da luz. Após aberto, consumir em até 30 dias</li>"
            "<li><strong>Ingredientes:</strong> Mix de frutas desidratadas (composição conforme safra)</li>"
            "<li>Sem açúcar adicionado · Sem conservantes · Vegano · 100% natural · Piedade/SP</li>"
            "</ul>"
            + SAIBAI_FOOTER
        ),
        "variants": [{"id": "gid://shopify/ProductVariant/53412771922238", "weight": 200}],
    },
    {
        "id": "gid://shopify/Product/12367499493694",
        "title": "Frutas Desidratadas - Pomar de Verão 200g",
        "productType": "Frutas Desidratadas",
        "tags": ["frutas", "desidratados", "snack", "natural", "pomar de verão", "piedade"],
        "seo": {
            "title": "Frutas Desidratadas Pomar de Verão 200g | Empório Saibai",
            "description": "Pomar de Verão: mix de frutas desidratadas com o sabor das estações mais quentes. 200g sem conservantes. Empório Saibai, Piedade/SP.",
        },
        "summary": "Pomar de Verão — mix de frutas desidratadas de estação, 200g. Sabor vibrante das frutas de verão o ano todo. Saibai, Piedade/SP.",
        "search_queries": ["frutas desidratadas verão", "pomar de verão", "snack saudável", "empório saibai"],
        "related": [FRUTAS[0]] + FRUTAS[2:],
        "complementary": CONSERVAS,
        "diet": FRUIT_DIET,
        "descriptionHtml": (
            "<p><strong>Pomar de Verão Saibai</strong> — capture a essência das estações mais quentes em 200g de frutas desidratadas artesanalmente em Piedade/SP.</p>"
            "<p>Frutas colhidas no ponto máximo de maturação e desidratadas lentamente para concentrar açúcar natural e intensidade de aromas. Textura única — nem seca demais, nem úmida — unindo doçura natural e nutrição essencial.</p>"
            "<ul>"
            "<li><strong>Verão o ano todo:</strong> Sabor vibrante das frutas de estação.</li>"
            "<li><strong>Artesanal e puro:</strong> Sem açúcares refinados ou corantes.</li>"
            "<li><strong>Momento gourmet:</strong> Chá da tarde, tábuas de queijos ou snack rápido.</li>"
            "</ul>"
            "<hr><p><strong>Sugestões de uso</strong></p>"
            "<ul>"
            "<li>Chá da tarde com queijos e castanhas.</li>"
            "<li>Ingredientes em trail mix e barrinhas caseiras.</li>"
            "<li>Decoração e recheio de bolos, muffins e pães artesanais.</li>"
            "</ul>"
            "<hr><p><strong>Ficha técnica</strong></p>"
            "<ul>"
            "<li><strong>Peso líquido:</strong> 200 g</li>"
            "<li><strong>Validade:</strong> 12 meses em embalagem fechada</li>"
            "<li><strong>Conservação:</strong> Local fresco, seco e ao abrigo da luz. Após aberto, consumir em até 30 dias</li>"
            "<li><strong>Ingredientes:</strong> Mix de frutas desidratadas de verão (composição conforme safra)</li>"
            "<li>Sem açúcar adicionado · Sem conservantes · Vegano · 100% natural · Piedade/SP</li>"
            "</ul>"
            + SAIBAI_FOOTER
        ),
        "variants": [{"id": "gid://shopify/ProductVariant/53412772348222", "weight": 200}],
    },
    {
        "id": "gid://shopify/Product/12367499886910",
        "title": "Maçã Desidratada Sem Casca 100g",
        "productType": "Frutas Desidratadas",
        "tags": ["frutas", "desidratados", "snack", "maca", "natural", "piedade"],
        "seo": {
            "title": "Maçã Desidratada Sem Casca 100g | Empório Saibai",
            "description": "Maçã desidratada sem casca, textura macia e sabor suave. Snack saudável e natural, sem aditivos. 100g. Empório Saibai, Piedade/SP.",
        },
        "summary": "Maçã desidratada sem casca, 100g. Textura macia, sabor suave, 100% natural. Snack saudável Empório Saibai, Piedade/SP.",
        "search_queries": ["maçã desidratada", "fruta seca", "snack saudável", "empório saibai"],
        "related": FRUTAS,
        "complementary": FRUTAS[3:5],
        "diet": FRUIT_DIET,
        "descriptionHtml": (
            "<p><strong>Maçã Desidratada Sem Casca Saibai</strong> — a leveza da maçã em sua forma mais pura, 100g de snack delicado produzido em Piedade/SP.</p>"
            "<p>Selecionada para quem aprecia textura macia e sabor suave que derrete na boca. Ao remover a casca, garantimos fatias tenras e fáceis de consumir — concentrado de frescor com curadoria Saibai.</p>"
            "<ul>"
            "<li><strong>Textura soft:</strong> Fatias tenras, sem rigidez da casca.</li>"
            "<li><strong>100% natural:</strong> Sem açúcares ou conservantes artificiais.</li>"
            "<li><strong>Snack ideal:</strong> Chá, lancheira infantil ou pausa saudável.</li>"
            "</ul>"
            "<hr><p><strong>Sugestões de uso</strong></p>"
            "<ul>"
            "<li>Lanche da tarde com chá verde ou camomila.</li>"
            "<li>Acrescentar a cereais, muesli e mix de nuts.</li>"
            "<li>Recheio de cookies, muffins e pães de mel artesanais.</li>"
            "</ul>"
            "<hr><p><strong>Ficha técnica</strong></p>"
            "<ul>"
            "<li><strong>Peso líquido:</strong> 100 g</li>"
            "<li><strong>Validade:</strong> 12 meses em embalagem fechada</li>"
            "<li><strong>Conservação:</strong> Local fresco, seco e ao abrigo da luz. Após aberto, consumir em até 20 dias</li>"
            "<li><strong>Ingredientes:</strong> Maçã desidratada sem casca</li>"
            "<li>Sem açúcar adicionado · Sem conservantes · Vegano · 100% natural · Piedade/SP</li>"
            "</ul>"
            + SAIBAI_FOOTER
        ),
        "variants": [{"id": "gid://shopify/ProductVariant/53412773888318", "weight": 100}],
    },
    {
        "id": "gid://shopify/Product/12367500050750",
        "title": "Abacaxi Desidratado 150g",
        "productType": "Frutas Desidratadas",
        "tags": ["frutas", "desidratados", "snack", "abacaxi", "natural", "piedade"],
        "seo": {
            "title": "Abacaxi Desidratado Selecionado 150g | Empório Saibai",
            "description": "Abacaxi desidratado com desidratação lenta para preservar o sabor tropical. Snack natural sem conservantes. 150g. Empório Saibai, Piedade/SP.",
        },
        "summary": "Abacaxi desidratado selecionado, 150g. Sabor tropical concentrado, desidratação lenta. Snack natural Saibai, Piedade/SP.",
        "search_queries": ["abacaxi desidratado", "fruta seca tropical", "snack natural", "empório saibai"],
        "related": FRUTAS,
        "complementary": FRUTAS[4:6],
        "diet": FRUIT_DIET,
        "descriptionHtml": (
            "<p><strong>Abacaxi Desidratado Selecionado Saibai</strong> — explosão de sabor tropical em 150g, desidratado lentamente em Piedade/SP.</p>"
            "<p>Processo que extrai apenas a água, concentrando açúcar natural e acidez característica. Snack suculento, textura firme e sabor que remete ao auge do verão — ingrediente versátil para gastronomia e bar.</p>"
            "<ul>"
            "<li><strong>Mixologia:</strong> Guarnição para Piña Colada, Gin Tônica e drinques tropicais.</li>"
            "<li><strong>Culinária:</strong> Saladas amargas e acompanhamento para carnes suínas.</li>"
            "<li><strong>Pureza total:</strong> 100% fruta, sem conservantes e sem açúcar adicionado.</li>"
            "</ul>"
            "<hr><p><strong>Sugestões de uso</strong></p>"
            "<ul>"
            "<li>Guarnição premium de coquetéis e mocktails.</li>"
            "<li>Salada tropical com rúcula, queijo de cabra e nozes.</li>"
            "<li>Snack energético ou topping de açaí e frozen yogurt.</li>"
            "</ul>"
            "<hr><p><strong>Ficha técnica</strong></p>"
            "<ul>"
            "<li><strong>Peso líquido:</strong> 150 g</li>"
            "<li><strong>Validade:</strong> 12 meses em embalagem fechada</li>"
            "<li><strong>Conservação:</strong> Local fresco, seco e ao abrigo da luz. Após aberto, consumir em até 20 dias</li>"
            "<li><strong>Ingredientes:</strong> Abacaxi desidratado</li>"
            "<li>Sem açúcar adicionado · Sem conservantes · Vegano · 100% natural · Piedade/SP</li>"
            "</ul>"
            + SAIBAI_FOOTER
        ),
        "variants": [{"id": "gid://shopify/ProductVariant/53412774478142", "weight": 150}],
    },
    {
        "id": "gid://shopify/Product/12367500214590",
        "title": "Manga Desidratada 100g",
        "productType": "Frutas Desidratadas",
        "tags": ["frutas", "desidratados", "snack", "manga", "natural", "piedade"],
        "seo": {
            "title": "Manga Desidratada Selecionada 100g | Empório Saibai",
            "description": "Manga desidratada suculenta no ápice da maturação. Snack natural com sabor intenso e concentrado. 100g. Empório Saibai, Piedade/SP.",
        },
        "summary": "Manga desidratada selecionada, 100g. Sabor intenso e concentrado, textura macia. Snack natural Empório Saibai, Piedade/SP.",
        "search_queries": ["manga desidratada", "fruta seca tropical", "snack natural", "empório saibai"],
        "related": FRUTAS,
        "complementary": FRUTAS[3:5],
        "diet": FRUIT_DIET,
        "descriptionHtml": (
            "<p><strong>Manga Desidratada Selecionada Saibai</strong> — intensidade tropical em 100g, frutas no ápice da maturação desidratadas em Piedade/SP.</p>"
            "<p>Desidratação lenta que preserva cor laranja vibrante e concentra aroma tropical. Textura macia e levemente elástica — explosão de sabor que remete ao mel natural da fruta.</p>"
            "<ul>"
            "<li><strong>Sabor incomparável:</strong> Naturalmente doce, sem açúcares ou corantes.</li>"
            "<li><strong>Textura gourmet:</strong> Mordida satisfatória em cada pedaço.</li>"
            "<li><strong>Energia pura:</strong> Fonte natural de vitaminas e fibras concentradas.</li>"
            "</ul>"
            "<hr><p><strong>Sugestões de uso</strong></p>"
            "<ul>"
            "<li>Snack tropical entre refeições ou pós-treino.</li>"
            "<li>Topping de bowls, iogurtes e sobremesas de colher.</li>"
            "<li>Ingredientes em barrinhas energéticas e trail mix premium.</li>"
            "</ul>"
            "<hr><p><strong>Ficha técnica</strong></p>"
            "<ul>"
            "<li><strong>Peso líquido:</strong> 100 g</li>"
            "<li><strong>Validade:</strong> 12 meses em embalagem fechada</li>"
            "<li><strong>Conservação:</strong> Local fresco, seco e ao abrigo da luz. Após aberto, consumir em até 20 dias</li>"
            "<li><strong>Ingredientes:</strong> Manga desidratada</li>"
            "<li>Sem açúcar adicionado · Sem conservantes · Vegano · 100% natural · Piedade/SP</li>"
            "</ul>"
            + SAIBAI_FOOTER
        ),
        "variants": [{"id": "gid://shopify/ProductVariant/53412774936894", "weight": 100}],
    },
    {
        "id": "gid://shopify/Product/12367500804414",
        "title": "Chaveiro Saibai",
        "productType": "Acessórios",
        "tags": ["acessorios", "decoracao", "souvenir", "chaveiro", "alcachofra", "piedade"],
        "seo": {
            "title": "Chaveiro Alcachofra Empório Saibai | Souvenir Exclusivo",
            "description": "Chaveiro exclusivo em formato de alcachofra, símbolo do Empório Saibai. Souvenir artesanal da fazenda em Piedade/SP. Design único e premium.",
        },
        "summary": "Chaveiro exclusivo em formato de alcachofra. Souvenir premium Empório Saibai, produção artesanal Piedade/SP. Edição limitada.",
        "search_queries": ["chaveiro saibai", "souvenir alcachofra", "presente empório saibai", "lembrança piedade"],
        "related": CONSERVAS,
        "complementary": CONSERVAS,
        "diet": [],
        "descriptionHtml": (
            "<p><strong>Chaveiro Alcachofra Empório Saibai</strong> — leve o charme da nossa fazenda em Piedade/SP sempre com você.</p>"
            "<p>Design autoral em formato de alcachofra (<em>Cynara scolymus</em>), símbolo de sofisticação e resistência. Acabamento premium em metal esmaltado — peça de colecionador para quem entende que a beleza está nas formas da natureza.</p>"
            "<ul>"
            "<li><strong>Design exclusivo:</strong> Formato icônico de alcachofra Saibai.</li>"
            "<li><strong>Versatilidade:</strong> Bag charm, chaveiro ou presente corporativo.</li>"
            "<li><strong>Presente ideal:</strong> Lembrança cheia de significado para amantes do lifestyle Saibai.</li>"
            "</ul>"
            "<hr><p><strong>Sugestões de uso</strong></p>"
            "<ul>"
            "<li>Souvenir de visita à fazenda ou evento Saibai.</li>"
            "<li>Presente para clientes, parceiros e amantes de gastronomia.</li>"
            "<li>Charm em bolsas, mochilas e chaves do carro.</li>"
            "</ul>"
            "<hr><p><strong>Informações do produto</strong></p>"
            "<ul>"
            "<li><strong>Material:</strong> Metal esmaltado com acabamento premium</li>"
            "<li><strong>Dimensões:</strong> Aprox. 4 cm de altura</li>"
            "<li><strong>Inclui:</strong> Argola metálica para chaves ou bolsa</li>"
            "<li>Produção exclusiva Empório Saibai · Piedade/SP · Edição limitada</li>"
            "</ul>"
            + SAIBAI_FOOTER
        ),
        "variants": [{"id": "gid://shopify/ProductVariant/53412776739134", "weight": 25}],
    },
]


def gql(query: str, variables: Optional[Dict[str, Any]] = None) -> dict:
    cmd = [
        "shopify", "store", "execute", "-s", STORE,
        "--allow-mutations", "-j", "-q", query,
    ]
    if variables:
        cmd.extend(["-v", json.dumps(variables)])
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    start = out.find("{")
    if start < 0:
        raise ValueError(f"Sem JSON: {out[:300]}")
    return json.loads(out[start:])


def build_metafields(item: Dict[str, Any]) -> List[Dict[str, str]]:
    mfs: List[Dict[str, str]] = [
        {"namespace": "custom", "key": "descri_o_do_produto", "type": "multi_line_text_field", "value": item["summary"]},
        {"namespace": "shopify--discovery--product_search_boost", "key": "queries", "type": "list.single_line_text_field", "value": json.dumps(item["search_queries"])},
        {"namespace": "shopify--discovery--product_recommendation", "key": "related_products", "type": "list.product_reference", "value": json.dumps(item["related"])},
        {"namespace": "shopify--discovery--product_recommendation", "key": "complementary_products", "type": "list.product_reference", "value": json.dumps(item["complementary"])},
        {"namespace": "mm-google-shopping", "key": "google_product_category", "type": "string", "value": GOOGLE_CAT},
    ]
    if item.get("food_taxonomy"):
        mfs.append({
            "namespace": "shopify", "key": "dietary-preferences",
            "type": "list.metaobject_reference", "value": json.dumps(item["diet"]),
        })
        mfs.append({
            "namespace": "shopify", "key": "food-product-form",
            "type": "list.metaobject_reference", "value": json.dumps([MO["food_outro"]]),
        })
    elif item["diet"]:
        mfs.append({
            "namespace": "shopify", "key": "dietary-preferences",
            "type": "list.metaobject_reference", "value": json.dumps(item["diet"]),
        })
    return mfs


def update_product(item: Dict[str, Any]) -> bool:
    q = """
    mutation productUpdate($input: ProductInput!) {
      productUpdate(input: $input) {
        product { id title vendor }
        userErrors { field message }
      }
    }
    """
    payload = {
        "id": item["id"],
        "vendor": VENDOR,
        "productType": item["productType"],
        "tags": item["tags"],
        "descriptionHtml": item["descriptionHtml"],
        "seo": item["seo"],
        "metafields": build_metafields(item),
    }
    r = gql(q, {"input": payload})
    errs = r.get("productUpdate", {}).get("userErrors", [])
    if errs:
        print(f"  ERRO produto {item['title']}: {errs[0]['message']}")
        return False
    return True


def update_variants(product_id: str, variants: List[Dict[str, Any]]) -> bool:
    if not variants:
        return True
    q = """
    mutation productVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
      productVariantsBulkUpdate(productId: $productId, variants: $variants) {
        productVariants { id }
        userErrors { field message }
      }
    }
    """
    payload = [
        {
            "id": v["id"],
            "inventoryItem": {
                "measurement": {"weight": {"value": float(v["weight"]), "unit": "GRAMS"}},
            },
        }
        for v in variants
    ]
    try:
        r = gql(q, {"productId": product_id, "variants": payload})
    except subprocess.CalledProcessError:
        print("  · peso variantes: pulado (API)")
        return True
    errs = r.get("productVariantsBulkUpdate", {}).get("userErrors", [])
    if errs:
        print(f"  · peso variantes: {errs[0]['message']}")
        return True
    return True


def remove_from_collection(collection_id: str, product_ids: List[str]) -> None:
    q = """
    mutation collectionRemoveProducts($id: ID!, $productIds: [ID!]!) {
      collectionRemoveProducts(id: $id, productIds: $productIds) {
        userErrors { field message }
      }
    }
    """
    r = gql(q, {"id": collection_id, "productIds": product_ids})
    errs = r.get("collectionRemoveProducts", {}).get("userErrors", [])
    if errs:
        print(f"  · coleção (já removido?): {errs[0]['message']}")


def main() -> int:
    print(f"Otimização completa — {len(PRODUCTS)} produtos\n")
    ok = 0
    for item in PRODUCTS:
        print(f"→ {item['title']}")
        p_ok = update_product(item)
        v_ok = update_variants(item["id"], item.get("variants", []))
        if item.get("remove_from_collection"):
            remove_from_collection(item["remove_from_collection"], [item["id"]])
        if p_ok and v_ok:
            ok += 1
            desc_len = len(item["descriptionHtml"])
            print(f"  OK | desc={desc_len} chars | tags={len(item['tags'])} | metafields=6+")
        time.sleep(0.4)
    print(f"\nConcluído: {ok}/{len(PRODUCTS)}")
    return 0 if ok == len(PRODUCTS) else 1


if __name__ == "__main__":
    sys.exit(main())

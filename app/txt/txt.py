from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag)

txt_vakancy="На поиски работы в Минске уходит много времени? Ищете сервис, где собраны актуальные вакансии: в Минске"#, Гомеле, Могилеве, Витебске, Бресте и Гродно?"
txt_vakancy2="В нашу базу ежедневно поступают наиболее актуальные предложения. Здесь найдется работа для опытных мастеров своего дела и начинающих специалистов без опыта"
content_adm=as_list(
  as_marked_section(
      Bold("Вам скоро ответят! Спасибо что вы с нами!"),
      " ",
      marker=" ",
  ),
  as_marked_section(
      Bold("Справочный гид:"),
      " /info_gid",
      marker="✅ ",
  ),
  #sep="\n\n",
  # as_marked_section(
  #     Bold("Summary:"),
  #     as_key_value("Total", 4),
  #     as_key_value("Success", 3),
  #     as_key_value("Failed", 1),
  #     marker="✅❌ ",
  # ),
  HashTag("#admin"),
  sep="\n\n")

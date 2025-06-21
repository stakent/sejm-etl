from transform.act_pdf_to_text import act_pdf_to_text


def replace_spaces_new_lines(text: str) -> str:
    text = text.replace("\n", "#")
    text = text.replace(" ", "_")
    return text


def test_pdf_to_text():
    file_name = "tests/transform/data/WDU20250000027.pdf"
    #  tests/transform/data/WDU20250000027.pdf

    with open(file_name, "rb") as f:
        text = act_pdf_to_text(pdf_file=f, act_position=27)
    assert " \n \n \n" not in text
    assert "Minister Sprawiedliwości" in text  # check if we process all pages
    # check if words splitting was reversed
    assert "wniosek o wydanie europejskiego nakazu aresztowania, zwanego dalej" in text
    # raise ValueError(replace_spaces_new_lines(text)[2531:2620])
    # check if page headers were removed
    assert (
        "stosuje się odpowiednio przepisy § 292–294 i § 296–298.”;\n4) po § 309a dodaje się"
        in text
    )

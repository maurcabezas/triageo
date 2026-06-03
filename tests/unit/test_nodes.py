from unittest.mock import MagicMock, patch
from app.graph.nodes import classify_ticket, retrieve_context, finalize_output, ClassificationResult


@patch("app.graph.nodes.get_chat_model")
def test_classify_ticket(mock_get_chat_model, base_state):
    # Mock the LLM and structured output
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    mock_get_chat_model.return_value = mock_llm
    mock_llm.with_structured_output.return_value = mock_structured_llm

    # Setup the mocked LLM output
    mock_structured_llm.invoke.return_value = ClassificationResult(
        category="billing",
        priority="high",
        confidence=0.85,
        reasoning="The ticket is clearly about subscription renewal issues."
    )

    # Execute classify_ticket node
    res = classify_ticket(base_state)

    # Verify predictions are extracted correctly
    assert res["category"] == "billing"
    assert res["priority"] == "high"
    assert res["confidence"] == 0.85
    assert res["reasoning"] == "The ticket is clearly about subscription renewal issues."

    mock_llm.with_structured_output.assert_called_once_with(ClassificationResult)
    mock_structured_llm.invoke.assert_called_once()


def test_retrieve_context(base_state):
    # Temporarily mock the module-level KB instance in nodes
    with patch("app.graph.nodes._kb") as mock_kb:
        mock_kb.retrieve.return_value = ["[billing] Billing FAQ: Check your invoice page."]
        
        res = retrieve_context(base_state)
        
        assert res == {"retrieved_context": ["[billing] Billing FAQ: Check your invoice page."]}
        mock_kb.retrieve.assert_called_once_with(
            base_state["subject"],
            base_state["description"]
        )


@patch("app.graph.nodes.save_ticket")
def test_finalize_output(mock_save_ticket, base_state):
    # Verify finalize_output calls save_ticket and returns empty dict
    res = finalize_output(base_state)
    assert res == {}
    mock_save_ticket.assert_called_once_with(base_state)

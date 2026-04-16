import pytest
from click.testing import CliRunner
from hncli.cli import cli

@pytest.fixture
def runner():
    return CliRunner()

def test_version(runner):
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert 'version 1.0.0' in result.output

def test_stories_mocked(runner, httpx_mock):
    # Mock topstories.json
    httpx_mock.add_response(
        url="https://hacker-news.firebaseio.com/v0/topstories.json",
        json=[1, 2]
    )
    # Mock individual items
    httpx_mock.add_response(
        url="https://hacker-news.firebaseio.com/v0/item/1.json",
        json={"id": 1, "title": "Test Story 1", "time": 1600000000, "descendants": 5}
    )
    httpx_mock.add_response(
        url="https://hacker-news.firebaseio.com/v0/item/2.json",
        json={"id": 2, "title": "Test Story 2", "time": 1600000001, "descendants": 10}
    )

    result = runner.invoke(cli, ['stories', '--limit', '2'])
    assert result.exit_code == 0
    assert 'Test Story 1' in result.output
    assert 'Test Story 2' in result.output
    assert '5' in result.output
    assert '10' in result.output

def test_comments_mocked(runner, httpx_mock):
    # Mock story item
    httpx_mock.add_response(
        url="https://hacker-news.firebaseio.com/v0/item/1.json",
        json={"id": 1, "kids": [101]}
    )
    # Mock comment item
    httpx_mock.add_response(
        url="https://hacker-news.firebaseio.com/v0/item/101.json",
        json={"id": 101, "by": "user1", "text": "This is a comment", "time": 1600000000}
    )

    result = runner.invoke(cli, ['comments', '1'])
    assert result.exit_code == 0
    assert 'by user1' in result.output
    assert 'This is a comment' in result.output

def test_comments_unescape_html(runner, httpx_mock):
    # Mock story item
    httpx_mock.add_response(
        url="https://hacker-news.firebaseio.com/v0/item/1.json",
        json={"id": 1, "kids": [102]}
    )
    # Mock comment item with HTML entities
    httpx_mock.add_response(
        url="https://hacker-news.firebaseio.com/v0/item/102.json",
        json={"id": 102, "by": "user2", "text": "It&#x27;s a &quot;test&quot; &amp; it works", "time": 1600000000}
    )

    result = runner.invoke(cli, ['comments', '1'])
    assert result.exit_code == 0
    assert "It's a \"test\" & it works" in result.output

def test_go_mocked(runner, httpx_mock, mocker):
    # Mock story item
    httpx_mock.add_response(
        url="https://hacker-news.firebaseio.com/v0/item/1.json",
        json={"id": 1, "url": "https://example.com"}
    )
    
    # Mock click.launch
    mock_launch = mocker.patch('click.launch')
    
    result = runner.invoke(cli, ['go', '1'])
    assert result.exit_code == 0
    mock_launch.assert_called_once_with('https://example.com')

def test_comment_launch(runner, mocker):
    # Mock click.launch
    mock_launch = mocker.patch('click.launch')
    
    result = runner.invoke(cli, ['comment', '1'])
    assert result.exit_code == 0
    mock_launch.assert_called_once_with('https://news.ycombinator.com/item?id=1')

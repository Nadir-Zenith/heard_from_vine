import marimo

__generated_with = "0.11.13"
app = marimo.App(width="full", layout_file="layouts/eda_feeds.grid.json")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell
def _(pd):
    df = pd.read_csv("./data/history.csv")
    df.head()
    return (df,)


@app.cell
def _(df):
    df_sorted = df.sort_values(by="published", ascending=False).reset_index()
    return (df_sorted,)


@app.cell
def _(df_sorted):
    df_sorted
    return


@app.cell
def _(df_sorted, mo):
    mo.accordion(
        {
            title : mo.md(f"{summary}") for title, summary in zip(df_sorted.title[:5], df_sorted.summary[:5])
        } 
    )
    return


@app.cell
def _(df_sorted):
    df_sorted.head()
    return


@app.cell
def _(df, mo):
    mo.carousel([
        mo.image(media_link) for media_link in df.media_content_0_url[:5]
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objs as go

app = Flask(__name__)

def fetch_data(assets, start_date, end_date):
    data = {}
    for asset, ticker in assets.items():
        data[asset] = yf.download(ticker, start=start_date, end=end_date)
    return data

def get_adjusted_closing_prices(data):
    prices = pd.DataFrame({asset: data[asset]['Adj Close'] for asset in data})
    prices.dropna(inplace=True)
    return prices

def calculate_total_returns(prices):
    initial_prices = prices.iloc[0]
    final_prices = prices.iloc[-1]
    total_returns = (final_prices - initial_prices) / initial_prices * 100
    total_returns_df = pd.DataFrame(total_returns, columns=['Total Return (%)'])
    return total_returns_df

def calculate_performance_metrics(prices):
    daily_returns = prices.pct_change().dropna()
    mean_returns = daily_returns.mean() * 252  # Annualized mean return
    volatility = daily_returns.std() * (252 ** 0.5)  # Annualized volatility
    sharpe_ratio = mean_returns / volatility  # Sharpe Ratio
    
    performance_metrics = pd.DataFrame({
        'Mean Return (%)': mean_returns * 100,
        'Volatility (%)': volatility * 100,
        'Sharpe Ratio': sharpe_ratio
    })
    return performance_metrics

def create_cumulative_returns_plot(cumulative_returns):
    cumulative_fig = go.Figure()
    for asset in cumulative_returns.columns:
        cumulative_fig.add_trace(go.Scatter(x=cumulative_returns.index, y=cumulative_returns[asset], mode='lines', name=asset))
    cumulative_fig.update_layout(title=f'Cumulative Returns', xaxis_title='Date', yaxis_title='Cumulative Return')
    return cumulative_fig

def create_performance_metrics_plot(performance_metrics, num_years):
    performance_fig = go.Figure()
    performance_fig.add_trace(go.Bar(x=performance_metrics.index, y=performance_metrics['Mean Return (%)'], name='Mean Return (%)'))
    performance_fig.add_trace(go.Bar(x=performance_metrics.index, y=performance_metrics['Volatility (%)'], name='Volatility (%)'))
    performance_fig.add_trace(go.Bar(x=performance_metrics.index, y=performance_metrics['Sharpe Ratio'], name='Sharpe Ratio'))
    performance_fig.update_layout(
        title=f'Performance Metrics over {num_years:.1f} Years',
        xaxis_title='Asset',
        yaxis_title='Value',
        barmode='group'
    )
    return performance_fig

def plot_total_returns(total_returns_df):
    total_returns_fig = px.bar(total_returns_df, x=total_returns_df.index, y='Total Return (%)', title='Total Returns')
    total_returns_fig.update_layout(template='plotly_dark')
    return total_returns_fig

@app.route('/')
def index():
    period = request.args.get('period', '10y')  # Default to 10 years if no period is specified
    selected_assets = request.args.getlist('assets')  # Get selected assets from checkboxes

    if not selected_assets:  # Default assets if none selected
        selected_assets = ['Gold', 'S&P 500', '10Y Treasury', 'Bitcoin']

    if period == '1y':
        start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    elif period == '5y':
        start_date = (datetime.today() - timedelta(days=5*365)).strftime('%Y-%m-%d')
    else:  # Default to 10 years
        start_date = (datetime.today() - timedelta(days=10*365)).strftime('%Y-%m-%d')

    end_date = datetime.today().strftime('%Y-%m-%d')

    assets = {
        'Gold': 'GC=F',
        'S&P 500': '^GSPC',
        '10Y Treasury': '^TNX',
        'Bitcoin': 'BTC-USD'
    }

    selected_data = {asset: assets[asset] for asset in selected_assets}

    data = fetch_data(selected_data, start_date, end_date)
    prices = get_adjusted_closing_prices(data)
    total_returns_df = calculate_total_returns(prices)
    performance_metrics = calculate_performance_metrics(prices)
    num_years = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days / 365.25
    cumulative_returns = prices.pct_change().add(1).cumprod().sub(1) * 100

    cumulative_fig = create_cumulative_returns_plot(cumulative_returns)
    performance_fig = create_performance_metrics_plot(performance_metrics, num_years)
    total_returns_fig = plot_total_returns(total_returns_df)

    return render_template('index.html', 
                           cumulative_fig=cumulative_fig.to_html(full_html=False),
                           performance_fig=performance_fig.to_html(full_html=False),
                           total_returns_fig=total_returns_fig.to_html(full_html=False),
                           selected_assets=selected_assets)

if __name__ == '__main__':
    app.run(debug=True)

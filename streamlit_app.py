import numpy as np
import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Stock Price Simulator (https://ac420example.streamlit.app/)",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Stock Price Simulator")

# Create the 4 requested tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Simulated Stock Demo",
    "2. App Source Code",
    "3. Code Sources & Attribution",
    "4. Theory & Help",
])

# ==========================================
# TAB 1: SIMULATED STOCK PRICE DEMO
# ==========================================
with tab1:
    st.header("Geometric Brownian Motion (GBM) Stock Simulator")
    st.markdown(
        "Adjust the market parameters below to simulate a hypothetical stock's "
        "price path over one trading year (252 trading days)."
    )

    # Sidebar or column controls for simulation parameters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ticker = st.text_input("Simulated Ticker", value="ACME")
        s0 = st.number_input("Initial Stock Price ($)", min_value=1.0, value=100.0, step=5.0)
    with col2:
        mu = st.slider(
            "Expected Annual Return (Drift, μ)",
            min_value=-0.50,
            max_value=0.50,
            value=0.08,
            step=0.01,
            format="%.2f",
        )
    with col3:
        sigma = st.slider(
            "Annual Volatility (σ)",
            min_value=0.05,
            max_value=1.00,
            value=0.20,
            step=0.01,
            format="%.2f",
        )
    with col4:
        seed = st.number_input("Random Seed", min_value=0, value=42, step=1)
        num_paths = st.slider("Number of Simulated Paths", min_value=1, max_value=10, value=1)

    # Simulation parameters (252 trading days in 1 year)
    T = 1.0
    N = 252
    dt = T / N

    # Run Geometric Brownian Motion simulation
    rng = np.random.default_rng(int(seed))
    # Generate standard normal random variables: shape (N, num_paths)
    z = rng.standard_normal((N, num_paths))

    # Calculate daily returns using exact GBM solution
    drift = (mu - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt) * z
    daily_log_returns = drift + diffusion

    # Prepend 0 for Day 0 (initial price) and compute cumulative price paths
    log_paths = np.vstack([np.zeros((1, num_paths)), np.cumsum(daily_log_returns, axis=0)])
    price_paths = s0 * np.exp(log_paths)

    # Format into a DataFrame for plotting
    columns = [f"{ticker} Path {i+1}" for i in range(num_paths)]
    df_prices = pd.DataFrame(price_paths, columns=columns)
    df_prices.index.name = "Trading Day"

    # Display key summary metrics for the primary path
    final_price = price_paths[-1, 0]
    pct_change = ((final_price - s0) / s0) * 100
    max_price = np.max(price_paths[:, 0])
    min_price = np.min(price_paths[:, 0])

    m1, m2, m3 = st.columns(3)
    m1.metric(f"{ticker} Ending Price (Path 1)", f"${final_price:,.2f}", f"{pct_change:+.2f}%")
    m2.metric("52-Week Simulated High (Path 1)", f"${max_price:,.2f}")
    m3.metric("52-Week Simulated Low (Path 1)", f"${min_price:,.2f}")

    # Plot the simulated prices
    st.line_chart(df_prices, y_label="Stock Price ($)", x_label="Trading Day")

    with st.expander("View Raw Simulated Data"):
        st.dataframe(df_prices.style.format("${:.2f}"), use_container_width=True)


# ==================================================================================
# TAB 2: (A) GITHUB LINK, (B) COLAB CODE (IF USED), (C) ACTUAL STREAMLIT PYTHON CODE
# ==================================================================================
with tab2:
    st.header("Full Application Source Code")
    st.markdown(
        "🔗 **GitHub Repository:** "
        "[https://github.com/wysocki-bu/AC420_example](https://github.com/wysocki-bu/AC420_example) "
    )
    st.info(
        "EX. 1: Below is the Python code powering this app (copied from Github Repository)."
    )

    example_code = '''import numpy as np
        import pandas as pd
        import streamlit as st
        etc.'''         
    st.code(example_code, language="python", line_numbers=True)

    st.info(
        "EX. 2: Below is the Python code powering this app, read dynamically from Github Repository."
    )

    try:
        with open(__file__, "r", encoding="utf-8") as f:
            source_code = f.read()
        st.code(source_code, language="python", line_numbers=True)
    except Exception as e:
        st.error(f"Could not read source file automatically: {e}")


# ==========================================
# TAB 3: CODE SOURCES & ATTRIBUTION
# ==========================================
with tab3:
    st.header("Code Sources, Libraries & Attribution")
    st.markdown(
        "This application was built by combining open-source Python libraries, "
        "standard finance formulas, and AI-assisted layout assistance."
    )

    st.subheader("1. AI Assistance")
    st.markdown(
        """
        * **LLM Code Generation (Google Gemini):** Used to scaffold the multi-tab Streamlit layout.
        """
    )

    st.subheader("2. Open-Source Libraries & Documentation")
    st.markdown(
        """
        * **Streamlit (`streamlit`):** Used for the web application framework, interactive widgets 
          (`st.tabs`, `st.slider`, `st.metric`), and native charting (`st.line_chart`). 
          *Reference: [Streamlit Documentation](https://streamlit.io)*
        * **NumPy (`numpy`):** Used for vectorized pseudo-random normal distribution sampling 
          (`np.random.default_rng`) and exponential cumulative sum calculations. 
          *Reference: [NumPy Random Sampling Docs](https://numpy.org)*
        * **Pandas (`pandas`):** Used to structure the time-series arrays into labeled DataFrames 
          for tabular inspection and plotting. 
          *Reference: [Pandas Documentation](https://pydata.org)*
        """
    )

    st.subheader("3. Mathematical & Financial References")
    st.markdown(
        """
        * **Geometric Brownian Motion (GBM) Discretization:** Adapted from standard quantitative 
          finance literature (e.g., John C. Hull, *Options, Futures, and Other Derivatives*), 
          using the exact analytical solution to the stochastic differential equation rather than 
          an Euler-Maruyama approximation to prevent negative stock prices.
        """
    )


# ==========================================
# TAB 4: THEORY & HELP PAGE
# ==========================================
with tab4:
    st.header("How Stock Prices Move: The Theory Behind the Simulation")
    st.markdown(
        """
        In real financial markets, stock prices move due to supply and demand driven by earnings 
        reports, macroeconomic news, interest rates, and investor sentiment. Because new information 
        arrives unpredictably, short-term price movements appear random.
        """
    )

    st.subheader("1. The Random Walk & Geometric Brownian Motion (GBM)")
    st.markdown(
        """
        Quantitative finance commonly models stock prices as a continuous-time stochastic process 
        called **Geometric Brownian Motion (GBM)**—the same foundational assumption used in the 
        famous Black-Scholes options pricing model.

        The change in a stock's price ($dS$) over a tiny step in time ($dt$) is governed by the 
        stochastic differential equation:
        """
    )
    st.latex(r"dS_t = \mu S_t \, dt + \sigma S_t \, dW_t")

    st.markdown(
        """
        This equation breaks stock movement into two distinct forces:
        1. **Deterministic Drift ($\mu S_t \, dt$):** The predictable trend or expected growth rate 
           ($\mu$) of the stock over time (e.g., reflecting long-term company growth and inflation).
        2. **Random Shock / Diffusion ($\sigma S_t \, dW_t$):** The unpredictable daily volatility 
           ($\sigma$) scaled by a Wiener process ($dW_t$), representing random market news and noise.
        """
    )

    st.subheader("2. Exact Simulation Formula Used in Tab 1")
    st.markdown(
        """
        To simulate daily prices over discrete steps ($\Delta t = \\frac{1}{252}$ years), we apply 
        Itô's Lemma to solve the equation above:
        """
    )
    st.latex(
        r"S_{t+\Delta t} = S_t \exp\left( \left(\mu - \frac{1}{2}\sigma^2\right)\Delta t + \sigma \sqrt{\Delta t} \, Z \right)"
    )
    st.markdown(
        """
        * **$S_t$**: Stock price at day $t$.
        * **$\mu$**: Expected annual return (Drift).
        * **$\sigma$**: Annualized volatility (standard deviation of returns).
        * **$Z$**: A random number drawn from a standard normal distribution ($Z \sim \mathcal{N}(0, 1)$).
        * **$-\frac{1}{2}\sigma^2$**: The *Itô correction term*, which accounts for the fact that 
          volatility drags down geometric compounding (e.g., a 50% drop followed by a 50% gain leaves 
          you at 75% of your starting value, not 100%).
        """
    )

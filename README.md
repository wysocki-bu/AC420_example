# AC420_example
Example for AC420 projeect: A Streamlit App with required documentation, code and information pages.

## 📈 This Repository is for a Example Stock Price Simulator & Required Documentation

An interactive multi-tab **Streamlit** web application that simulates stock price trajectories, displays its own live source code, documents its code attributions, and explains the finance theory behind stock price movements.

---

## ✨ Features

The app is organized into four interactive tabs:

1. **Simulated Stock Demo:** 
   * Configure initial stock price ($S_0$), expected annual return/drift ($\mu$), annual volatility ($\sigma$), random seed, and the number of simulated paths.
   * Visualizes a 252-trading-day (1-year) price simulation with summary metrics (Ending Price, 52-Week High, 52-Week Low) and an expandable raw data table.
2. **App Source Code:** 
   * Dynamically reads and displays the exact Python script running the application alongside a link to this repository.
3. **Code Sources & Attribution:** 
   * Summarizes the open-source libraries, mathematical references, and AI tools used to build the project.
4. **Theory & Help:** 
   * Provides an accessible breakdown of the Random Walk hypothesis, Geometric Brownian Motion (GBM), Itô's Lemma, and real-world market limitations (fat tails, volatility clustering, and price jumps).

---

## Included Python Libraries

* **[Streamlit](https://streamlit.io)** – Interactive web UI, layout tabs, and native charting
* **[NumPy](https://numpy.org)** – Vectorized pseudo-random normal sampling and stochastic path calculations
* **[Pandas](https://pydata.org)** – Time-series structuring and tabular formatting

---

## 📐 Mathematical Model

Stock price paths are generated using the exact analytical solution to the Geometric Brownian Motion stochastic differential equation:

$$S_{t+\Delta t} = S_t \exp\left( \left(\mu - \frac{1}{2}\sigma^2\right)\Delta t + \sigma \sqrt{\Delta t} \, Z \right)$$

Where:
* $S_t$ = Stock price at time $t$
* $\mu$ = Expected annualized return (drift)
* $\sigma$ = Annualized volatility
* $\Delta t$ = Time step ($\frac{1}{252}$ trading years)
* $Z \sim \mathcal{N}(0, 1)$ = Standard normal random shock

---

## ⚠️ Disclaimer

This app example is intended strictly for **educational and demonstration purposes**.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import math
import os
from typing import List

def BlackScholes(S, K, T, r, sigma, optionType) -> List[float]:
    T = T / 365  # Convert T to years
    d1 = (math.log(S / K) + (r + (sigma ** 2) / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    if optionType == "call":
        callPrice = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
        
        # Greeks
        delta = norm.cdf(d1)
        gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
        theta = -((S * sigma * norm.pdf(d1)) / (2 * math.sqrt(T))) - r * K * math.exp(-r * T) * norm.cdf(d2)
        vega = (S * norm.pdf(d1) * math.sqrt(T)) / 100  # Vega per 1% change in volatility
        rho = K * T * math.exp(-r * T) * norm.cdf(d2) / 100 # Rho per 1% change in risk free rate
        
        return [round(d1, 3), round(d2, 3), round(callPrice, 2), round(delta, 3), round(gamma, 3), round(theta / 365, 3), round(vega, 3), round(rho, 3)]
    
    elif optionType == "put":
        putPrice = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
        # Greeks
        delta = norm.cdf(d1) - 1
        gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
        theta = -((S * sigma * norm.pdf(d1)) / (2 * math.sqrt(T))) + r * K * math.exp(-r * T) * norm.cdf(-d2)
        vega = (S * norm.pdf(d1) * math.sqrt(T)) / 100  # Vega per 1% change in volatility
        rho = (-K * T * math.exp(-r * T) * norm.cdf(-d2)) / 100 # Rho per 1% change in risk free rate
        
        return [round(d1, 3), round(d2, 3), round(putPrice, 2), round(delta, 3), round(gamma, 3), round(theta / 365, 3), round(vega, 3), round(rho, 3)]
    
    else: 
        raise ValueError("Invalid option type. Please enter 'call' or 'put'.")


def visualizePrice(S, K, T, r, sigma, optionType):
    S_values = np.linspace(0.01, 2 * S, 100)
    prices = []
    
    for S_val in S_values:
        result = BlackScholes(S_val, K, T, r, sigma, optionType)
        prices.append(result[2])
    
    plt.figure(figsize=(8, 6))
    plt.title("Option Price")
    plt.plot(S_values, prices)
    plt.xlabel('Underlying Asset Price')
    plt.ylabel('Option Price')
    plt.grid(True)
    
    if not os.path.exists('./plots'):
        os.makedirs('./plots')
    
    plt.savefig('./plots/option_price.png')
    plt.show()

def visualizeGreek(S, K, T, r, sigma, optionType, greek_name, greek_index):
    S_values = np.linspace(0.01, 2 * S, 100)
    greek_values = []
    
    for S_val in S_values:
        result = BlackScholes(S_val, K, T, r, sigma, optionType)
        greek_values.append(result[greek_index])
    
    plt.figure(figsize=(8, 6))
    plt.title(greek_name)
    plt.plot(S_values, greek_values)
    plt.xlabel('Underlying Asset Price')
    plt.ylabel(greek_name)
    plt.grid(True)
    
    if not os.path.exists('./plots'):
        os.makedirs('./plots')
    
    plt.savefig(f'./plots/{greek_name.lower()}.png')
    plt.show()

def main():
    S = float(input("Enter the Price of the underlying asset: "))
    K = float(input("Enter a Strike Price: "))
    T = float(input("Enter a Time to Maturity (in days): "))
    r = float(input("Enter a Risk Free Rate (annualized in 0.xx format): "))
    sigma = float(input("Enter a Volatility (annualized in x.xx format): "))
    optionType = input("Enter an Option Type (call/put): ")
    
    results = BlackScholes(S, K, T, r, sigma, optionType)
    
    print(f"d1: {results[0]}")
    print(f"d2: {results[1]}")
    print(f"Price: {results[2]}\n")
    print(f"Delta: {results[3]}") 
    print(f"Gamma: {results[4]}") 
    print(f"Theta: {results[5]}") 
    print(f"Vega: {results[6]}") 
    print(f"Rho: {results[7]}") 
    
    # Visualize option price
    visualizePrice(S, K, T, r, sigma, optionType)
    
    # Visualize Greeks
    visualizeGreek(S, K, T, r, sigma, optionType, "Delta", 3)
    visualizeGreek(S, K, T, r, sigma, optionType, "Gamma", 4)
    visualizeGreek(S, K, T, r, sigma, optionType, "Theta", 5)
    visualizeGreek(S, K, T, r, sigma, optionType, "Vega", 6)
    visualizeGreek(S, K, T, r, sigma, optionType, "Rho", 7)

if __name__ == "__main__":
    main()

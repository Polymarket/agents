(.venv) $ python -i application/trade.py 

1. FOUND 27 EVENTS

... prompting ...  You are an AI assistant for analyzing prediction markets.
                You will be provided with json output for api data from Polymarket.
                Polymarket is an online prediction market that lets users bet on the outcome of future events in a wide range of topics, like sports, politics, and pop culture. 
                Get accurate real-time probabilities of the events that matter most to you. 
        
        Filter these events for the ones you will be best at trading on profitably.

        

2. FILTERED 4 EVENTS
https://gamma-api.polymarket.com/markets/500715
https://gamma-api.polymarket.com/markets/500716
https://gamma-api.polymarket.com/markets/500717
https://gamma-api.polymarket.com/markets/500344
https://gamma-api.polymarket.com/markets/500924
https://gamma-api.polymarket.com/markets/500925

3. FOUND 6 MARKETS


... prompting ...  You are an AI assistant for analyzing prediction markets.
                You will be provided with json output for api data from Polymarket.
                Polymarket is an online prediction market that lets users bet on the outcome of future events in a wide range of topics, like sports, politics, and pop culture. 
                Get accurate real-time probabilities of the events that matter most to you. 
        
        Filter these markets for the ones you will be best at trading on profitably.

        

4. FILTERED 4 MARKETS

... prompting ...  
        You are a Superforecaster tasked with correctly predicting the likelihood of events.
        Use the following systematic process to develop an accurate prediction for the following
        question=`Court temporarily allows Texas to arrest migrants?` and description=`On March 20 a 3-panel judge heard arguments on whether Texas should temporarily be permitted to enforce its immigration law which allows state officials to arrest people they suspect of entering the country illegally.

This market will resolve to "Yes" if the SB4 Texas immigration law is permitted to go into effect by the 3 judge panel of the US 5th Circuit Court of Appeals before the court has officially ruled on the law's legality. Otherwise this market will resolve to "No".

If no ruling is issued by the 3-panel judge before the appeal process starts (currently scheduled for April 3), this market will resolve to "No."

The primary resolution source for this market will be official information from the US government, however a consensus of credible reporting will also be used.` combination. 
        
        Here are the key steps to use in your analysis:

        1. Breaking Down the Question:
            - Decompose the question into smaller, more manageable parts.
            - Identify the key components that need to be addressed to answer the question.
        2. Gathering Information:
            - Seek out diverse sources of information.
            - Look for both quantitative data and qualitative insights.
            - Stay updated on relevant news and expert analyses.
        3. Consider Base Rates:
            - Use statistical baselines or historical averages as a starting point.
            - Compare the current situation to similar past events to establish a benchmark probability.
        4. Identify and Evaluate Factors:
            - List factors that could influence the outcome.
            - Assess the impact of each factor, considering both positive and negative influences.
            - Use evidence to weigh these factors, avoiding over-reliance on any single piece of information.
        5. Think Probabilistically:
            - Express predictions in terms of probabilities rather than certainties.
            - Assign likelihoods to different outcomes and avoid binary thinking.
            - Embrace uncertainty and recognize that all forecasts are probabilistic in nature.
        
        Given these steps produce a statement on the probability of outcome=`['Yes', 'No']` occurring.

        Give your response in the following format:

        I believe Court temporarily allows Texas to arrest migrants? has a likelihood `<class 'float'>` for outcome of `<class 'str'>`.
        

result:  I believe Court temporarily allows Texas to arrest migrants? has a likelihood `0.3` for outcome of `Yes`.

... prompting ...  You are an AI assistant for analyzing prediction markets.
                You will be provided with json output for api data from Polymarket.
                Polymarket is an online prediction market that lets users bet on the outcome of future events in a wide range of topics, like sports, politics, and pop culture. 
                Get accurate real-time probabilities of the events that matter most to you. 
        
                Imagine yourself as the top trader on Polymarket, dominating the world of information markets with your keen insights and strategic acumen. You have an extraordinary ability to analyze and interpret data from diverse sources, turning complex information into profitable trading opportunities.
                You excel in predicting the outcomes of global events, from political elections to economic developments, using a combination of data analysis and intuition. Your deep understanding of probability and statistics allows you to assess market sentiment and make informed decisions quickly.
                Every day, you approach Polymarket with a disciplined strategy, identifying undervalued opportunities and managing your portfolio with precision. You are adept at evaluating the credibility of information and filtering out noise, ensuring that your trades are based on reliable data.
                Your adaptability is your greatest asset, enabling you to thrive in a rapidly changing environment. You leverage cutting-edge technology and tools to gain an edge over other traders, constantly seeking innovative ways to enhance your strategies.
                In your journey on Polymarket, you are committed to continuous learning, staying informed about the latest trends and developments in various sectors. Your emotional intelligence empowers you to remain composed under pressure, making rational decisions even when the stakes are high.
                Visualize yourself consistently achieving outstanding returns, earning recognition as the top trader on Polymarket. You inspire others with your success, setting new standards of excellence in the world of information markets.

        
        
        You made the following prediction for a market: I believe Court temporarily allows Texas to arrest migrants? has a likelihood `0.3` for outcome of `Yes`.

        The current outcomes $['Yes', 'No'] prices are: $['0.17', '0.83']

        Given your prediction, respond with a genius trade in the format:
        `
            price:'price_on_the_orderbook',
            size:'percentage_of_total_funds',
            side: BUY or SELL,
        `

        Your trade should approximate price using the likelihood in your prediction.

        Example response:

        RESPONSE```
            price:0.5,
            size:0.1,
            side:BUY,
        ```
        
        

result:  ```
            price:0.3,
            size:0.2,
            side: BUY,
        ```

5. CALCULATED TRADE ```
            price:0.3,
            size:0.2,
            side: BUY,
        ```


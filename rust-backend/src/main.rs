#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    use twitter_v2::{authorization::BearerToken, TwitterApi};
    use dotenv::dotenv;
    use std::env;
    dotenv().ok();

    let auth = BearerToken::new(env::var("BEARER_TOKEN").expect("BEARER_TOKEN must be set"));
    let res = TwitterApi::new(auth)
        .get_tweets_search_recent("rustlang".to_string())
        .max_results(100)
        .send()
        .await?
        .into_data()
        .unwrap();

    let mut i: i32 = 0;
    for tweet in res {
        let first_10_chars = tweet.text.chars().take(80).collect::<String>();
        println!("Index: {}, ID: {}, Text: {}", i, tweet.id, first_10_chars);
        i = i + 1;
    }
    Ok(())
}
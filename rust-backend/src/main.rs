use rand::Rng;

fn generate_random_string(length: usize) -> String {
    let characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let mut rng = rand::thread_rng();

    (0..length)
        .map(|_| {
            let idx = rng.gen_range(0..characters.len());
            characters.chars().nth(idx).unwrap()
        })
        .collect()
}


#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    use twitter_v2::{authorization::BearerToken, TwitterApi};
    use dotenv::dotenv;
    use std::env;
    use std::time::Instant;

    dotenv().ok();

    let auth2 = BearerToken::new(env::var("BEARER_TOKEN").expect("BEARER_TOKEN must be set"));
    let random_string = generate_random_string(10);
    let start = Instant::now();

    let res2 = TwitterApi::new(auth2)
        .get_tweets_search_recent("rustlang".to_string())
        .max_results(100)
        .send()
        .await?
        .into_data()
        .unwrap();

    let duration = start.elapsed();

    println!("Time elapsed in retrieval is: {:?}", duration);

    let mut i: i32 = 0;
    for tweet in res2 {
        let first_10_chars = tweet.text.chars().take(80).collect::<String>();
        println!("Index: {}, ID: {}, Text: {}", i, tweet.id, first_10_chars);
        i = i + 1;
    }
    Ok(())
}
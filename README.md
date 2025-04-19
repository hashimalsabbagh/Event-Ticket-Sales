**What the project does:**

- This is a project which aims to host and sell event tickets to customers for event holders. 
- Users can register on the site, add money to their wallet, buy tickets, and ask for refunds.

**Initial commit:**

- Added Event, reservations, cancellation request (refund), and wallet models
- Developed register and login pages, event page, wallet page, and current reservations page
- Developed backend logic for buying tickets
  1. max amount of tickets a user can buy
  2. not allowing user to buy tickets of the same event if they already have a reservation to the same event
  3. error when quantity is more than current amount of tickets
  4.  error when user doesn't have enough money)
- Developed backend logic for wallet 
  1. no more than 10,000 can be added at once
  2. money changes according to event buying and refunding
- Developed backend logic for reservation cancelling 
  1. request goes to admin which they can accept or reject
  2. shows status to be pending until admin's answer
  3. doesn't allow user to request a refund again on the same reservation once rejected

**Secondary commit:**

- Added Transaction model to record wallet transactions
- Modified cancellation request model to keep a record of refund history
- Modified wallet and reservation pages
  1. Wallet page was modified to show the list of transactions made by the user (amount deducted or added)
  2. Reservation page was modified to show a separate list of current and previous cancel requests that have been requested by the user and their status (rejected, accepted, or pending)
  
  

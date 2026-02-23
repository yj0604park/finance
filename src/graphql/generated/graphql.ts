import { gql } from '@apollo/client';
import * as Apollo from '@apollo/client';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
export type MakeEmpty<T extends { [key: string]: unknown }, K extends keyof T> = { [_ in K]?: never };
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
const defaultOptions = {} as const;
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string; }
  String: { input: string; output: string; }
  Boolean: { input: boolean; output: boolean; }
  Int: { input: number; output: number; }
  Float: { input: number; output: number; }
  /** Date (isoformat) */
  Date: { input: string; output: string; }
  /** Date with time (isoformat) */
  DateTime: { input: string; output: string; }
  /** Decimal (fixed-point) */
  Decimal: { input: string; output: string; }
  /** The `JSON` scalar type represents JSON values as specified by [ECMA-404](https://ecma-international.org/wp-content/uploads/ECMA-404_2nd_edition_december_2017.pdf). */
  JSON: { input: Record<string, unknown>; output: Record<string, unknown>; }
};

export type AccountFilter = {
  AND: InputMaybe<AccountFilter>;
  DISTINCT: InputMaybe<Scalars['Boolean']['input']>;
  NOT: InputMaybe<AccountFilter>;
  OR: InputMaybe<AccountFilter>;
  amount: InputMaybe<DecimalComparisonFilterLookup>;
  bank: BankFilter;
  currency: InputMaybe<CurrencyTypeFilterLookup>;
  id: InputMaybe<IdBaseFilterLookup>;
  isActive: InputMaybe<BoolBaseFilterLookup>;
  lastUpdate: InputMaybe<DatetimeDatetimeFilterLookup>;
  name: InputMaybe<StrFilterLookup>;
  type: InputMaybe<AccountTypeFilterLookup>;
};

export type AccountInput = {
  bank: OneToManyInput;
  currency: InputMaybe<CurrencyType>;
  name: Scalars['String']['input'];
  type: InputMaybe<AccountType>;
};

export type AccountNode = Node & {
  __typename?: 'AccountNode';
  amount: Scalars['Decimal']['output'];
  bank: BankNode;
  currency: CurrencyType;
  firstTransaction: Maybe<Scalars['Date']['output']>;
  id: Scalars['ID']['output'];
  isActive: Scalars['Boolean']['output'];
  lastTransaction: Maybe<Scalars['Date']['output']>;
  lastUpdate: Maybe<Scalars['DateTime']['output']>;
  name: Scalars['String']['output'];
  type: AccountType;
};

/** A connection to a list of items. */
export type AccountNodeConnection = {
  __typename?: 'AccountNodeConnection';
  /** Contains the nodes in this connection */
  edges: Array<AccountNodeEdge>;
  /** Pagination data for this connection */
  pageInfo: PageInfo;
  /** Total quantity of existing nodes. */
  totalCount: Maybe<Scalars['Int']['output']>;
};

/** An edge in a connection. */
export type AccountNodeEdge = {
  __typename?: 'AccountNodeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String']['output'];
  /** The item at the end of the edge */
  node: AccountNode;
};

export type AccountOrder = {
  bank: InputMaybe<BankOrder>;
  lastUpdate: InputMaybe<Ordering>;
  name: InputMaybe<Ordering>;
};

export enum AccountType {
  CheckingAccount = 'CHECKING_ACCOUNT',
  CreditCard = 'CREDIT_CARD',
  InstallmentSaving = 'INSTALLMENT_SAVING',
  Loan = 'LOAN',
  SavingsAccount = 'SAVINGS_ACCOUNT',
  Stock = 'STOCK',
  TimeDeposit = 'TIME_DEPOSIT'
}

export type AccountTypeFilterLookup = {
  /** Case-sensitive containment test. Filter will be skipped on `null` value */
  contains: InputMaybe<AccountType>;
  /** Case-sensitive ends-with. Filter will be skipped on `null` value */
  endsWith: InputMaybe<AccountType>;
  /** Exact match. Filter will be skipped on `null` value */
  exact: InputMaybe<AccountType>;
  /** Case-insensitive containment test. Filter will be skipped on `null` value */
  iContains: InputMaybe<AccountType>;
  /** Case-insensitive ends-with. Filter will be skipped on `null` value */
  iEndsWith: InputMaybe<AccountType>;
  /** Case-insensitive exact match. Filter will be skipped on `null` value */
  iExact: InputMaybe<AccountType>;
  /** Case-insensitive regular expression match. Filter will be skipped on `null` value */
  iRegex: InputMaybe<AccountType>;
  /** Case-insensitive starts-with. Filter will be skipped on `null` value */
  iStartsWith: InputMaybe<AccountType>;
  /** Exact match of items in a given list. Filter will be skipped on `null` value */
  inList: InputMaybe<Array<AccountType>>;
  /** Assignment test. Filter will be skipped on `null` value */
  isNull: InputMaybe<Scalars['Boolean']['input']>;
  /** Case-sensitive regular expression match. Filter will be skipped on `null` value */
  regex: InputMaybe<AccountType>;
  /** Case-sensitive starts-with. Filter will be skipped on `null` value */
  startsWith: InputMaybe<AccountType>;
};

export type AmazonOrderInput = {
  date: Scalars['Date']['input'];
  isReturned: InputMaybe<Scalars['Boolean']['input']>;
  item: Scalars['String']['input'];
  returnTransaction: InputMaybe<OneToManyInput>;
  transaction: InputMaybe<OneToManyInput>;
};

export type AmazonOrderNode = Node & {
  __typename?: 'AmazonOrderNode';
  date: Scalars['Date']['output'];
  id: Scalars['ID']['output'];
  isReturned: Scalars['Boolean']['output'];
  item: Scalars['String']['output'];
  returnTransaction: Maybe<TransactionNode>;
  transaction: Maybe<TransactionNode>;
};

/** A connection to a list of items. */
export type AmazonOrderNodeConnection = {
  __typename?: 'AmazonOrderNodeConnection';
  /** Contains the nodes in this connection */
  edges: Array<AmazonOrderNodeEdge>;
  /** Pagination data for this connection */
  pageInfo: PageInfo;
  /** Total quantity of existing nodes. */
  totalCount: Maybe<Scalars['Int']['output']>;
};

/** An edge in a connection. */
export type AmazonOrderNodeEdge = {
  __typename?: 'AmazonOrderNodeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String']['output'];
  /** The item at the end of the edge */
  node: AmazonOrderNode;
};

export type AmazonOrderOrder = {
  date: InputMaybe<Ordering>;
};

export type AmountSnapshotFilter = {
  AND: InputMaybe<AmountSnapshotFilter>;
  DISTINCT: InputMaybe<Scalars['Boolean']['input']>;
  NOT: InputMaybe<AmountSnapshotFilter>;
  OR: InputMaybe<AmountSnapshotFilter>;
  currency: InputMaybe<CurrencyTypeFilterLookup>;
  date: InputMaybe<DateDateFilterLookup>;
  id: InputMaybe<IdBaseFilterLookup>;
};

export type AmountSnapshotNode = Node & {
  __typename?: 'AmountSnapshotNode';
  amount: Scalars['Decimal']['output'];
  currency: CurrencyType;
  date: Scalars['Date']['output'];
  id: Scalars['ID']['output'];
  summary: Maybe<Scalars['JSON']['output']>;
};

/** A connection to a list of items. */
export type AmountSnapshotNodeConnection = {
  __typename?: 'AmountSnapshotNodeConnection';
  /** Contains the nodes in this connection */
  edges: Array<AmountSnapshotNodeEdge>;
  /** Pagination data for this connection */
  pageInfo: PageInfo;
  /** Total quantity of existing nodes. */
  totalCount: Maybe<Scalars['Int']['output']>;
};

/** An edge in a connection. */
export type AmountSnapshotNodeEdge = {
  __typename?: 'AmountSnapshotNodeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String']['output'];
  /** The item at the end of the edge */
  node: AmountSnapshotNode;
};

export type AmountSnapshotOrder = {
  date: InputMaybe<Ordering>;
  name: InputMaybe<Ordering>;
};

export type BankBalance = {
  __typename?: 'BankBalance';
  currency: Scalars['String']['output'];
  value: Scalars['Decimal']['output'];
};

export type BankFilter = {
  AND: InputMaybe<BankFilter>;
  DISTINCT: InputMaybe<Scalars['Boolean']['input']>;
  NOT: InputMaybe<BankFilter>;
  OR: InputMaybe<BankFilter>;
  id: InputMaybe<IdBaseFilterLookup>;
  name: InputMaybe<StrFilterLookup>;
};

export type BankNode = Node & {
  __typename?: 'BankNode';
  accountSet: AccountNodeConnection;
  balance: Array<BankBalance>;
  id: Scalars['ID']['output'];
  name: Scalars['String']['output'];
};


export type BankNodeAccountSetArgs = {
  after?: InputMaybe<Scalars['String']['input']>;
  before?: InputMaybe<Scalars['String']['input']>;
  filters: InputMaybe<AccountFilter>;
  first?: InputMaybe<Scalars['Int']['input']>;
  last?: InputMaybe<Scalars['Int']['input']>;
  order: InputMaybe<AccountOrder>;
};

/** A connection to a list of items. */
export type BankNodeConnection = {
  __typename?: 'BankNodeConnection';
  /** Contains the nodes in this connection */
  edges: Array<BankNodeEdge>;
  /** Pagination data for this connection */
  pageInfo: PageInfo;
  /** Total quantity of existing nodes. */
  totalCount: Maybe<Scalars['Int']['output']>;
};

/** An edge in a connection. */
export type BankNodeEdge = {
  __typename?: 'BankNodeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String']['output'];
  /** The item at the end of the edge */
  node: BankNode;
};

export type BankOrder = {
  name: InputMaybe<Ordering>;
};

export type BoolBaseFilterLookup = {
  /** Exact match. Filter will be skipped on `null` value */
  exact: InputMaybe<Scalars['Boolean']['input']>;
  /** Exact match of items in a given list. Filter will be skipped on `null` value */
  inList: InputMaybe<Array<Scalars['Boolean']['input']>>;
  /** Assignment test. Filter will be skipped on `null` value */
  isNull: InputMaybe<Scalars['Boolean']['input']>;
};

export enum CurrencyType {
  Krw = 'KRW',
  Usd = 'USD'
}

export type CurrencyTypeFilterLookup = {
  /** Case-sensitive containment test. Filter will be skipped on `null` value */
  contains: InputMaybe<CurrencyType>;
  /** Case-sensitive ends-with. Filter will be skipped on `null` value */
  endsWith: InputMaybe<CurrencyType>;
  /** Exact match. Filter will be skipped on `null` value */
  exact: InputMaybe<CurrencyType>;
  /** Case-insensitive containment test. Filter will be skipped on `null` value */
  iContains: InputMaybe<CurrencyType>;
  /** Case-insensitive ends-with. Filter will be skipped on `null` value */
  iEndsWith: InputMaybe<CurrencyType>;
  /** Case-insensitive exact match. Filter will be skipped on `null` value */
  iExact: InputMaybe<CurrencyType>;
  /** Case-insensitive regular expression match. Filter will be skipped on `null` value */
  iRegex: InputMaybe<CurrencyType>;
  /** Case-insensitive starts-with. Filter will be skipped on `null` value */
  iStartsWith: InputMaybe<CurrencyType>;
  /** Exact match of items in a given list. Filter will be skipped on `null` value */
  inList: InputMaybe<Array<CurrencyType>>;
  /** Assignment test. Filter will be skipped on `null` value */
  isNull: InputMaybe<Scalars['Boolean']['input']>;
  /** Case-sensitive regular expression match. Filter will be skipped on `null` value */
  regex: InputMaybe<CurrencyType>;
  /** Case-sensitive starts-with. Filter will be skipped on `null` value */
  startsWith: InputMaybe<CurrencyType>;
};

export type DateDateFilterLookup = {
  day: InputMaybe<IntComparisonFilterLookup>;
  /** Exact match. Filter will be skipped on `null` value */
  exact: InputMaybe<Scalars['Date']['input']>;
  /** Greater than. Filter will be skipped on `null` value */
  gt: InputMaybe<Scalars['Date']['input']>;
  /** Greater than or equal to. Filter will be skipped on `null` value */
  gte: InputMaybe<Scalars['Date']['input']>;
  /** Exact match of items in a given list. Filter will be skipped on `null` value */
  inList: InputMaybe<Array<Scalars['Date']['input']>>;
  /** Assignment test. Filter will be skipped on `null` value */
  isNull: InputMaybe<Scalars['Boolean']['input']>;
  isoWeekDay: InputMaybe<IntComparisonFilterLookup>;
  isoYear: InputMaybe<IntComparisonFilterLookup>;
  /** Less than. Filter will be skipped on `null` value */
  lt: InputMaybe<Scalars['Date']['input']>;
  /** Less than or equal to. Filter will be skipped on `null` value */
  lte: InputMaybe<Scalars['Date']['input']>;
  month: InputMaybe<IntComparisonFilterLookup>;
  quarter: InputMaybe<IntComparisonFilterLookup>;
  /** Inclusive range test (between) */
  range: InputMaybe<DateRangeLookup>;
  week: InputMaybe<IntComparisonFilterLookup>;
  weekDay: InputMaybe<IntComparisonFilterLookup>;
  year: InputMaybe<IntComparisonFilterLookup>;
};

export type DateRangeLookup = {
  end: InputMaybe<Scalars['Date']['input']>;
  start: InputMaybe<Scalars['Date']['input']>;
};

export type DatetimeDatetimeFilterLookup = {
  date: InputMaybe<IntComparisonFilterLookup>;
  day: InputMaybe<IntComparisonFilterLookup>;
  /** Exact match. Filter will be skipped on `null` value */
  exact: InputMaybe<Scalars['DateTime']['input']>;
  /** Greater than. Filter will be skipped on `null` value */
  gt: InputMaybe<Scalars['DateTime']['input']>;
  /** Greater than or equal to. Filter will be skipped on `null` value */
  gte: InputMaybe<Scalars['DateTime']['input']>;
  hour: InputMaybe<IntComparisonFilterLookup>;
  /** Exact match of items in a given list. Filter will be skipped on `null` value */
  inList: InputMaybe<Array<Scalars['DateTime']['input']>>;
  /** Assignment test. Filter will be skipped on `null` value */
  isNull: InputMaybe<Scalars['Boolean']['input']>;
  isoWeekDay: InputMaybe<IntComparisonFilterLookup>;
  isoYear: InputMaybe<IntComparisonFilterLookup>;
  /** Less than. Filter will be skipped on `null` value */
  lt: InputMaybe<Scalars['DateTime']['input']>;
  /** Less than or equal to. Filter will be skipped on `null` value */
  lte: InputMaybe<Scalars['DateTime']['input']>;
  minute: InputMaybe<IntComparisonFilterLookup>;
  month: InputMaybe<IntComparisonFilterLookup>;
  quarter: InputMaybe<IntComparisonFilterLookup>;
  /** Inclusive range test (between) */
  range: InputMaybe<DatetimeRangeLookup>;
  second: InputMaybe<IntComparisonFilterLookup>;
  time: InputMaybe<IntComparisonFilterLookup>;
  week: InputMaybe<IntComparisonFilterLookup>;
  weekDay: InputMaybe<IntComparisonFilterLookup>;
  year: InputMaybe<IntComparisonFilterLookup>;
};

export type DatetimeRangeLookup = {
  end: InputMaybe<Scalars['DateTime']['input']>;
  start: InputMaybe<Scalars['DateTime']['input']>;
};

export type DecimalComparisonFilterLookup = {
  /** Exact match. Filter will be skipped on `null` value */
  exact: InputMaybe<Scalars['Decimal']['input']>;
  /** Greater than. Filter will be skipped on `null` value */
  gt: InputMaybe<Scalars['Decimal']['input']>;
  /** Greater than or equal to. Filter will be skipped on `null` value */
  gte: InputMaybe<Scalars['Decimal']['input']>;
  /** Exact match of items in a given list. Filter will be skipped on `null` value */
  inList: InputMaybe<Array<Scalars['Decimal']['input']>>;
  /** Assignment test. Filter will be skipped on `null` value */
  isNull: InputMaybe<Scalars['Boolean']['input']>;
  /** Less than. Filter will be skipped on `null` value */
  lt: InputMaybe<Scalars['Decimal']['input']>;
  /** Less than or equal to. Filter will be skipped on `null` value */
  lte: InputMaybe<Scalars['Decimal']['input']>;
  /** Inclusive range test (between) */
  range: InputMaybe<DecimalRangeLookup>;
};

export type DecimalRangeLookup = {
  end: InputMaybe<Scalars['Decimal']['input']>;
  start: InputMaybe<Scalars['Decimal']['input']>;
};

export type IdBaseFilterLookup = {
  /** Exact match. Filter will be skipped on `null` value */
  exact: InputMaybe<Scalars['ID']['input']>;
  /** Exact match of items in a given list. Filter will be skipped on `null` value */
  inList: InputMaybe<Array<Scalars['ID']['input']>>;
  /** Assignment test. Filter will be skipped on `null` value */
  isNull: InputMaybe<Scalars['Boolean']['input']>;
};

export type IntComparisonFilterLookup = {
  /** Exact match. Filter will be skipped on `null` value */
  exact: InputMaybe<Scalars['Int']['input']>;
  /** Greater than. Filter will be skipped on `null` value */
  gt: InputMaybe<Scalars['Int']['input']>;
  /** Greater than or equal to. Filter will be skipped on `null` value */
  gte: InputMaybe<Scalars['Int']['input']>;
  /** Exact match of items in a given list. Filter will be skipped on `null` value */
  inList: InputMaybe<Array<Scalars['Int']['input']>>;
  /** Assignment test. Filter will be skipped on `null` value */
  isNull: InputMaybe<Scalars['Boolean']['input']>;
  /** Less than. Filter will be skipped on `null` value */
  lt: InputMaybe<Scalars['Int']['input']>;
  /** Less than or equal to. Filter will be skipped on `null` value */
  lte: InputMaybe<Scalars['Int']['input']>;
  /** Inclusive range test (between) */
  range: InputMaybe<IntRangeLookup>;
};

export type IntRangeLookup = {
  end: InputMaybe<Scalars['Int']['input']>;
  start: InputMaybe<Scalars['Int']['input']>;
};

export type Mutation = {
  __typename?: 'Mutation';
  createAccount: AccountNode;
  createAmazonOrder: AmazonOrderNode;
  createRetailer: RetailerNode;
  createStock: StockNode;
  createStockTransaction: StockTransactionNode;
  createTransaction: TransactionNode;
};


export type MutationCreateAccountArgs = {
  data: AccountInput;
};


export type MutationCreateAmazonOrderArgs = {
  data: AmazonOrderInput;
};


export type MutationCreateRetailerArgs = {
  data: RetailerInput;
};


export type MutationCreateStockArgs = {
  data: StockInput;
};


export type MutationCreateStockTransactionArgs = {
  data: StockTransactionInput;
};


export type MutationCreateTransactionArgs = {
  data: TransactionInput;
};

/** An object with a Globally Unique ID */
export type Node = {
  /** The Globally Unique ID of this object */
  id: Scalars['ID']['output'];
};

export type OneToManyInput = {
  set: InputMaybe<Scalars['ID']['input']>;
};

export enum Ordering {
  Asc = 'ASC',
  AscNullsFirst = 'ASC_NULLS_FIRST',
  AscNullsLast = 'ASC_NULLS_LAST',
  Desc = 'DESC',
  DescNullsFirst = 'DESC_NULLS_FIRST',
  DescNullsLast = 'DESC_NULLS_LAST'
}

/** Information to aid in pagination. */
export type PageInfo = {
  __typename?: 'PageInfo';
  /** When paginating forwards, the cursor to continue. */
  endCursor: Maybe<Scalars['String']['output']>;
  /** When paginating forwards, are there more items? */
  hasNextPage: Scalars['Boolean']['output'];
  /** When paginating backwards, are there more items? */
  hasPreviousPage: Scalars['Boolean']['output'];
  /** When paginating backwards, the cursor to continue. */
  startCursor: Maybe<Scalars['String']['output']>;
};

export type Query = {
  __typename?: 'Query';
  accountRelay: AccountNodeConnection;
  amazonOrderRelay: AmazonOrderNodeConnection;
  amountSnapshotRelay: AmountSnapshotNodeConnection;
  bankRelay: BankNodeConnection;
  retailerRelay: RetailerNodeConnection;
  salaryRelay: SalaryNodeConnection;
  salarySummary: Array<SalarySummaryNode>;
  salaryYears: Array<Scalars['Int']['output']>;
  stockRelay: StockNodeConnection;
  transactionRelay: TransactionNodeConnection;
};


export type QueryAccountRelayArgs = {
  after?: InputMaybe<Scalars['String']['input']>;
  before?: InputMaybe<Scalars['String']['input']>;
  filters: InputMaybe<AccountFilter>;
  first?: InputMaybe<Scalars['Int']['input']>;
  last?: InputMaybe<Scalars['Int']['input']>;
  order: InputMaybe<AccountOrder>;
};


export type QueryAmazonOrderRelayArgs = {
  after?: InputMaybe<Scalars['String']['input']>;
  before?: InputMaybe<Scalars['String']['input']>;
  first?: InputMaybe<Scalars['Int']['input']>;
  last?: InputMaybe<Scalars['Int']['input']>;
  order: InputMaybe<AmazonOrderOrder>;
};


export type QueryAmountSnapshotRelayArgs = {
  after?: InputMaybe<Scalars['String']['input']>;
  before?: InputMaybe<Scalars['String']['input']>;
  filters: InputMaybe<AmountSnapshotFilter>;
  first?: InputMaybe<Scalars['Int']['input']>;
  last?: InputMaybe<Scalars['Int']['input']>;
  order: InputMaybe<AmountSnapshotOrder>;
};


export type QueryBankRelayArgs = {
  after?: InputMaybe<Scalars['String']['input']>;
  before?: InputMaybe<Scalars['String']['input']>;
  filters: InputMaybe<BankFilter>;
  first?: InputMaybe<Scalars['Int']['input']>;
  last?: InputMaybe<Scalars['Int']['input']>;
};


export type QueryRetailerRelayArgs = {
  after?: InputMaybe<Scalars['String']['input']>;
  before?: InputMaybe<Scalars['String']['input']>;
  filters: InputMaybe<RetailerFilter>;
  first?: InputMaybe<Scalars['Int']['input']>;
  last?: InputMaybe<Scalars['Int']['input']>;
};


export type QuerySalaryRelayArgs = {
  after?: InputMaybe<Scalars['String']['input']>;
  before?: InputMaybe<Scalars['String']['input']>;
  filters: InputMaybe<SalaryFilter>;
  first?: InputMaybe<Scalars['Int']['input']>;
  last?: InputMaybe<Scalars['Int']['input']>;
  order: InputMaybe<SalaryOrder>;
};


export type QueryStockRelayArgs = {
  after?: InputMaybe<Scalars['String']['input']>;
  before?: InputMaybe<Scalars['String']['input']>;
  first?: InputMaybe<Scalars['Int']['input']>;
  last?: InputMaybe<Scalars['Int']['input']>;
};


export type QueryTransactionRelayArgs = {
  after?: InputMaybe<Scalars['String']['input']>;
  before?: InputMaybe<Scalars['String']['input']>;
  filters: InputMaybe<TransactionFilter>;
  first?: InputMaybe<Scalars['Int']['input']>;
  last?: InputMaybe<Scalars['Int']['input']>;
  order: InputMaybe<TransactionOrder>;
};

export type RetailerFilter = {
  AND: InputMaybe<RetailerFilter>;
  DISTINCT: InputMaybe<Scalars['Boolean']['input']>;
  NOT: InputMaybe<RetailerFilter>;
  OR: InputMaybe<RetailerFilter>;
  category: InputMaybe<TransactionCategoryFilterLookup>;
  id: InputMaybe<IdBaseFilterLookup>;
  name: InputMaybe<StrFilterLookup>;
};

export type RetailerInput = {
  category: InputMaybe<TransactionCategory>;
  name: Scalars['String']['input'];
  type: InputMaybe<RetailerType>;
};

export type RetailerNode = Node & {
  __typename?: 'RetailerNode';
  category: TransactionCategory;
  id: Scalars['ID']['output'];
  name: Scalars['String']['output'];
};

/** A connection to a list of items. */
export type RetailerNodeConnection = {
  __typename?: 'RetailerNodeConnection';
  /** Contains the nodes in this connection */
  edges: Array<RetailerNodeEdge>;
  /** Pagination data for this connection */
  pageInfo: PageInfo;
  /** Total quantity of existing nodes. */
  totalCount: Maybe<Scalars['Int']['output']>;
};

/** An edge in a connection. */
export type RetailerNodeEdge = {
  __typename?: 'RetailerNodeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String']['output'];
  /** The item at the end of the edge */
  node: RetailerNode;
};

export enum RetailerType {
  Bank = 'BANK',
  Etc = 'ETC',
  Income = 'INCOME',
  Person = 'PERSON',
  Restaurant = 'RESTAURANT',
  Service = 'SERVICE',
  Store = 'STORE'
}

export type SalaryFilter = {
  AND: InputMaybe<SalaryFilter>;
  DISTINCT: InputMaybe<Scalars['Boolean']['input']>;
  NOT: InputMaybe<SalaryFilter>;
  OR: InputMaybe<SalaryFilter>;
  date: InputMaybe<DateDateFilterLookup>;
  id: InputMaybe<IdBaseFilterLookup>;
};

export type SalaryNode = Node & {
  __typename?: 'SalaryNode';
  adjustmentDetail: Scalars['JSON']['output'];
  date: Scalars['Date']['output'];
  deductionDetail: Scalars['JSON']['output'];
  grossPay: Scalars['Decimal']['output'];
  id: Scalars['ID']['output'];
  netPay: Scalars['Decimal']['output'];
  payDetail: Scalars['JSON']['output'];
  taxDetail: Scalars['JSON']['output'];
  totalAdjustment: Scalars['Decimal']['output'];
  totalDeduction: Scalars['Decimal']['output'];
  totalWithheld: Scalars['Decimal']['output'];
  transaction: TransactionNode;
};

/** A connection to a list of items. */
export type SalaryNodeConnection = {
  __typename?: 'SalaryNodeConnection';
  /** Contains the nodes in this connection */
  edges: Array<SalaryNodeEdge>;
  /** Pagination data for this connection */
  pageInfo: PageInfo;
  /** Total quantity of existing nodes. */
  totalCount: Maybe<Scalars['Int']['output']>;
};

/** An edge in a connection. */
export type SalaryNodeEdge = {
  __typename?: 'SalaryNodeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String']['output'];
  /** The item at the end of the edge */
  node: SalaryNode;
};

export type SalaryOrder = {
  date: InputMaybe<Ordering>;
};

export type SalarySummaryNode = {
  __typename?: 'SalarySummaryNode';
  totalGrossPay: Scalars['Decimal']['output'];
  year: Scalars['Int']['output'];
};

export type StockInput = {
  currency: InputMaybe<CurrencyType>;
  name: Scalars['String']['input'];
  ticker: InputMaybe<Scalars['String']['input']>;
};

export type StockNode = Node & {
  __typename?: 'StockNode';
  currency: CurrencyType;
  id: Scalars['ID']['output'];
  name: Scalars['String']['output'];
  ticker: Maybe<Scalars['String']['output']>;
};

/** A connection to a list of items. */
export type StockNodeConnection = {
  __typename?: 'StockNodeConnection';
  /** Contains the nodes in this connection */
  edges: Array<StockNodeEdge>;
  /** Pagination data for this connection */
  pageInfo: PageInfo;
  /** Total quantity of existing nodes. */
  totalCount: Maybe<Scalars['Int']['output']>;
};

/** An edge in a connection. */
export type StockNodeEdge = {
  __typename?: 'StockNodeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String']['output'];
  /** The item at the end of the edge */
  node: StockNode;
};

export type StockTransactionInput = {
  account: OneToManyInput;
  amount: Scalars['Decimal']['input'];
  date: Scalars['Date']['input'];
  note: InputMaybe<Scalars['String']['input']>;
  price: Scalars['Decimal']['input'];
  relatedTransaction: InputMaybe<OneToManyInput>;
  shares: Scalars['Decimal']['input'];
  stock: OneToManyInput;
};

export type StockTransactionNode = Node & {
  __typename?: 'StockTransactionNode';
  account: AccountNode;
  amount: Scalars['Decimal']['output'];
  id: Scalars['ID']['output'];
  note: Maybe<Scalars['String']['output']>;
  price: Scalars['Decimal']['output'];
  relatedTransaction: TransactionNode;
  shares: Scalars['Decimal']['output'];
  stock: StockNode;
};

export type StrFilterLookup = {
  /** Case-sensitive containment test. Filter will be skipped on `null` value */
  contains: InputMaybe<Scalars['String']['input']>;
  /** Case-sensitive ends-with. Filter will be skipped on `null` value */
  endsWith: InputMaybe<Scalars['String']['input']>;
  /** Exact match. Filter will be skipped on `null` value */
  exact: InputMaybe<Scalars['String']['input']>;
  /** Case-insensitive containment test. Filter will be skipped on `null` value */
  iContains: InputMaybe<Scalars['String']['input']>;
  /** Case-insensitive ends-with. Filter will be skipped on `null` value */
  iEndsWith: InputMaybe<Scalars['String']['input']>;
  /** Case-insensitive exact match. Filter will be skipped on `null` value */
  iExact: InputMaybe<Scalars['String']['input']>;
  /** Case-insensitive regular expression match. Filter will be skipped on `null` value */
  iRegex: InputMaybe<Scalars['String']['input']>;
  /** Case-insensitive starts-with. Filter will be skipped on `null` value */
  iStartsWith: InputMaybe<Scalars['String']['input']>;
  /** Exact match of items in a given list. Filter will be skipped on `null` value */
  inList: InputMaybe<Array<Scalars['String']['input']>>;
  /** Assignment test. Filter will be skipped on `null` value */
  isNull: InputMaybe<Scalars['Boolean']['input']>;
  /** Case-sensitive regular expression match. Filter will be skipped on `null` value */
  regex: InputMaybe<Scalars['String']['input']>;
  /** Case-sensitive starts-with. Filter will be skipped on `null` value */
  startsWith: InputMaybe<Scalars['String']['input']>;
};

export enum TransactionCategory {
  Cash = 'CASH',
  Clothing = 'CLOTHING',
  DailyNecessity = 'DAILY_NECESSITY',
  EatOut = 'EAT_OUT',
  Etc = 'ETC',
  Grocery = 'GROCERY',
  Housing = 'HOUSING',
  Income = 'INCOME',
  Interest = 'INTEREST',
  Leisure = 'LEISURE',
  Medical = 'MEDICAL',
  Membership = 'MEMBERSHIP',
  Parenting = 'PARENTING',
  Present = 'PRESENT',
  Service = 'SERVICE',
  Stock = 'STOCK',
  Transfer = 'TRANSFER',
  Transportation = 'TRANSPORTATION'
}

export type TransactionCategoryFilterLookup = {
  /** Case-sensitive containment test. Filter will be skipped on `null` value */
  contains: InputMaybe<TransactionCategory>;
  /** Case-sensitive ends-with. Filter will be skipped on `null` value */
  endsWith: InputMaybe<TransactionCategory>;
  /** Exact match. Filter will be skipped on `null` value */
  exact: InputMaybe<TransactionCategory>;
  /** Case-insensitive containment test. Filter will be skipped on `null` value */
  iContains: InputMaybe<TransactionCategory>;
  /** Case-insensitive ends-with. Filter will be skipped on `null` value */
  iEndsWith: InputMaybe<TransactionCategory>;
  /** Case-insensitive exact match. Filter will be skipped on `null` value */
  iExact: InputMaybe<TransactionCategory>;
  /** Case-insensitive regular expression match. Filter will be skipped on `null` value */
  iRegex: InputMaybe<TransactionCategory>;
  /** Case-insensitive starts-with. Filter will be skipped on `null` value */
  iStartsWith: InputMaybe<TransactionCategory>;
  /** Exact match of items in a given list. Filter will be skipped on `null` value */
  inList: InputMaybe<Array<TransactionCategory>>;
  /** Assignment test. Filter will be skipped on `null` value */
  isNull: InputMaybe<Scalars['Boolean']['input']>;
  /** Case-sensitive regular expression match. Filter will be skipped on `null` value */
  regex: InputMaybe<TransactionCategory>;
  /** Case-sensitive starts-with. Filter will be skipped on `null` value */
  startsWith: InputMaybe<TransactionCategory>;
};

export type TransactionFilter = {
  AND: InputMaybe<TransactionFilter>;
  DISTINCT: InputMaybe<Scalars['Boolean']['input']>;
  NOT: InputMaybe<TransactionFilter>;
  OR: InputMaybe<TransactionFilter>;
  account: AccountFilter;
  date: InputMaybe<DateDateFilterLookup>;
  id: InputMaybe<IdBaseFilterLookup>;
};

export type TransactionInput = {
  account: OneToManyInput;
  amount: Scalars['Decimal']['input'];
  date: Scalars['Date']['input'];
  isInternal: InputMaybe<Scalars['Boolean']['input']>;
  note: InputMaybe<Scalars['String']['input']>;
  retailer: InputMaybe<OneToManyInput>;
  type: InputMaybe<TransactionCategory>;
};

export type TransactionNode = Node & {
  __typename?: 'TransactionNode';
  account: AccountNode;
  amount: Scalars['Decimal']['output'];
  balance: Maybe<Scalars['Decimal']['output']>;
  date: Scalars['Date']['output'];
  getSortingAmount: Scalars['Float']['output'];
  id: Scalars['ID']['output'];
  isInternal: Scalars['Boolean']['output'];
  note: Maybe<Scalars['String']['output']>;
  relatedTransaction: Maybe<TransactionNode>;
  requiresDetail: Scalars['Boolean']['output'];
  retailer: Maybe<RetailerNode>;
  reviewed: Scalars['Boolean']['output'];
  type: TransactionCategory;
};

/** A connection to a list of items. */
export type TransactionNodeConnection = {
  __typename?: 'TransactionNodeConnection';
  /** Contains the nodes in this connection */
  edges: Array<TransactionNodeEdge>;
  /** Pagination data for this connection */
  pageInfo: PageInfo;
  /** Total quantity of existing nodes. */
  totalCount: Maybe<Scalars['Int']['output']>;
};

/** An edge in a connection. */
export type TransactionNodeEdge = {
  __typename?: 'TransactionNodeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String']['output'];
  /** The item at the end of the edge */
  node: TransactionNode;
};

export type TransactionOrder = {
  account: InputMaybe<AccountOrder>;
  amount: InputMaybe<Ordering>;
  balance: InputMaybe<Ordering>;
  date: InputMaybe<Ordering>;
  id: InputMaybe<Ordering>;
};

/** One possible value for a given Enum. Enum values are unique values, not a placeholder for a string or numeric value. However an Enum value is returned in a JSON response as a string. */
export type __EnumValue = {
  __typename?: '__EnumValue';
  name: Scalars['String']['output'];
  description: Maybe<Scalars['String']['output']>;
  isDeprecated: Scalars['Boolean']['output'];
  deprecationReason: Maybe<Scalars['String']['output']>;
};

/** Object and Interface types are described by a list of Fields, each of which has a name, potentially a list of arguments, and a return type. */
export type __Field = {
  __typename?: '__Field';
  name: Scalars['String']['output'];
  description: Maybe<Scalars['String']['output']>;
  args: Array<__InputValue>;
  type: __Type;
  isDeprecated: Scalars['Boolean']['output'];
  deprecationReason: Maybe<Scalars['String']['output']>;
};


/** Object and Interface types are described by a list of Fields, each of which has a name, potentially a list of arguments, and a return type. */
export type __FieldArgsArgs = {
  includeDeprecated?: InputMaybe<Scalars['Boolean']['input']>;
};

/** Arguments provided to Fields or Directives and the input fields of an InputObject are represented as Input Values which describe their type and optionally a default value. */
export type __InputValue = {
  __typename?: '__InputValue';
  name: Scalars['String']['output'];
  description: Maybe<Scalars['String']['output']>;
  type: __Type;
  /** A GraphQL-formatted string representing the default value for this input value. */
  defaultValue: Maybe<Scalars['String']['output']>;
  isDeprecated: Scalars['Boolean']['output'];
  deprecationReason: Maybe<Scalars['String']['output']>;
};

/**
 * The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.
 *
 * Depending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name, description and optional `specifiedByURL`, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.
 */
export type __Type = {
  __typename?: '__Type';
  kind: __TypeKind;
  name: Maybe<Scalars['String']['output']>;
  description: Maybe<Scalars['String']['output']>;
  specifiedByURL: Maybe<Scalars['String']['output']>;
  fields: Maybe<Array<__Field>>;
  interfaces: Maybe<Array<__Type>>;
  possibleTypes: Maybe<Array<__Type>>;
  enumValues: Maybe<Array<__EnumValue>>;
  inputFields: Maybe<Array<__InputValue>>;
  ofType: Maybe<__Type>;
  isOneOf: Maybe<Scalars['Boolean']['output']>;
};


/**
 * The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.
 *
 * Depending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name, description and optional `specifiedByURL`, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.
 */
export type __TypeFieldsArgs = {
  includeDeprecated?: InputMaybe<Scalars['Boolean']['input']>;
};


/**
 * The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.
 *
 * Depending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name, description and optional `specifiedByURL`, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.
 */
export type __TypeEnumValuesArgs = {
  includeDeprecated?: InputMaybe<Scalars['Boolean']['input']>;
};


/**
 * The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.
 *
 * Depending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name, description and optional `specifiedByURL`, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.
 */
export type __TypeInputFieldsArgs = {
  includeDeprecated?: InputMaybe<Scalars['Boolean']['input']>;
};

/** An enum describing what kind of type a given `__Type` is. */
export enum __TypeKind {
  /** Indicates this type is a scalar. */
  Scalar = 'SCALAR',
  /** Indicates this type is an object. `fields` and `interfaces` are valid fields. */
  Object = 'OBJECT',
  /** Indicates this type is an interface. `fields`, `interfaces`, and `possibleTypes` are valid fields. */
  Interface = 'INTERFACE',
  /** Indicates this type is a union. `possibleTypes` is a valid field. */
  Union = 'UNION',
  /** Indicates this type is an enum. `enumValues` is a valid field. */
  Enum = 'ENUM',
  /** Indicates this type is an input object. `inputFields` is a valid field. */
  InputObject = 'INPUT_OBJECT',
  /** Indicates this type is a list. `ofType` is a valid field. */
  List = 'LIST',
  /** Indicates this type is a non-null. `ofType` is a valid field. */
  NonNull = 'NON_NULL'
}

export type CreateRetailerMutationVariables = Exact<{
  name: Scalars['String']['input'];
  type: RetailerType;
  category: TransactionCategory;
}>;


export type CreateRetailerMutation = { __typename?: 'Mutation', createRetailer: { __typename?: 'RetailerNode', id: string, name: string, category: TransactionCategory } };

export type CreateTransactionMutationVariables = Exact<{
  amount: Scalars['Decimal']['input'];
  date: Scalars['Date']['input'];
  accountId: InputMaybe<Scalars['ID']['input']>;
  isInternal: InputMaybe<Scalars['Boolean']['input']>;
  note: InputMaybe<Scalars['String']['input']>;
  retailerId: InputMaybe<Scalars['ID']['input']>;
}>;


export type CreateTransactionMutation = { __typename?: 'Mutation', createTransaction: { __typename?: 'TransactionNode', id: string } };

export type CreateTransactionWithoutRetailerMutationVariables = Exact<{
  amount: Scalars['Decimal']['input'];
  date: Scalars['Date']['input'];
  accountId: InputMaybe<Scalars['ID']['input']>;
  isInternal: InputMaybe<Scalars['Boolean']['input']>;
  note: InputMaybe<Scalars['String']['input']>;
}>;


export type CreateTransactionWithoutRetailerMutation = { __typename?: 'Mutation', createTransaction: { __typename?: 'TransactionNode', id: string } };

export type GetAccountListQueryVariables = Exact<{
  after: Scalars['String']['input'];
  bankId: InputMaybe<Scalars['ID']['input']>;
  isActive: InputMaybe<BoolBaseFilterLookup>;
}>;


export type GetAccountListQuery = { __typename?: 'Query', accountRelay: { __typename?: 'AccountNodeConnection', totalCount: number | null, edges: Array<{ __typename?: 'AccountNodeEdge', cursor: string, node: { __typename?: 'AccountNode', amount: string, name: string, currency: CurrencyType, lastUpdate: string | null, id: string, isActive: boolean, type: AccountType, firstTransaction: string | null, lastTransaction: string | null, bank: { __typename?: 'BankNode', id: string, name: string } } }>, pageInfo: { __typename?: 'PageInfo', hasNextPage: boolean, hasPreviousPage: boolean, startCursor: string | null, endCursor: string | null } } };

export type GetSimpleAccountListQueryVariables = Exact<{
  bankId: InputMaybe<Scalars['ID']['input']>;
}>;


export type GetSimpleAccountListQuery = { __typename?: 'Query', accountRelay: { __typename?: 'AccountNodeConnection', edges: Array<{ __typename?: 'AccountNodeEdge', node: { __typename?: 'AccountNode', id: string, name: string } }> } };

export type GetAccountDetailQueryVariables = Exact<{
  accountId: InputMaybe<Scalars['ID']['input']>;
}>;


export type GetAccountDetailQuery = { __typename?: 'Query', accountRelay: { __typename?: 'AccountNodeConnection', edges: Array<{ __typename?: 'AccountNodeEdge', node: { __typename?: 'AccountNode', amount: string, name: string, currency: CurrencyType, lastUpdate: string | null, id: string, isActive: boolean, type: AccountType, firstTransaction: string | null, lastTransaction: string | null, bank: { __typename?: 'BankNode', id: string, name: string } } }> } };

export type GetAccountTypeQueryVariables = Exact<{ [key: string]: never; }>;


export type GetAccountTypeQuery = { __typename?: 'Query', __type: { __typename?: '__Type', enumValues: Array<{ __typename?: '__EnumValue', name: string }> | null } | null };

export type GetBankListQueryVariables = Exact<{ [key: string]: never; }>;


export type GetBankListQuery = { __typename?: 'Query', bankRelay: { __typename?: 'BankNodeConnection', edges: Array<{ __typename?: 'BankNodeEdge', node: { __typename?: 'BankNode', id: string, name: string, balance: Array<{ __typename?: 'BankBalance', currency: string, value: string }>, accountSet: { __typename?: 'AccountNodeConnection', totalCount: number | null, edges: Array<{ __typename?: 'AccountNodeEdge', node: { __typename?: 'AccountNode', type: AccountType, id: string, currency: CurrencyType, amount: string, lastUpdate: string | null, name: string, isActive: boolean } }> } } }> } };

export type GetBankSimpleListQueryVariables = Exact<{ [key: string]: never; }>;


export type GetBankSimpleListQuery = { __typename?: 'Query', bankRelay: { __typename?: 'BankNodeConnection', edges: Array<{ __typename?: 'BankNodeEdge', node: { __typename?: 'BankNode', id: string, name: string } }> } };

export type GetRetailerListQueryVariables = Exact<{
  after: InputMaybe<Scalars['String']['input']>;
}>;


export type GetRetailerListQuery = { __typename?: 'Query', retailerRelay: { __typename?: 'RetailerNodeConnection', totalCount: number | null, edges: Array<{ __typename?: 'RetailerNodeEdge', node: { __typename?: 'RetailerNode', id: string, name: string, category: TransactionCategory } }>, pageInfo: { __typename?: 'PageInfo', hasNextPage: boolean, endCursor: string | null } } };

export type GetRetailerTypeQueryVariables = Exact<{ [key: string]: never; }>;


export type GetRetailerTypeQuery = { __typename?: 'Query', __type: { __typename?: '__Type', name: string | null, enumValues: Array<{ __typename?: '__EnumValue', name: string }> | null } | null };

export type GetSalaryListQueryVariables = Exact<{ [key: string]: never; }>;


export type GetSalaryListQuery = { __typename?: 'Query', salaryRelay: { __typename?: 'SalaryNodeConnection', totalCount: number | null, edges: Array<{ __typename?: 'SalaryNodeEdge', node: { __typename?: 'SalaryNode', date: string, grossPay: string, id: string, netPay: string, totalDeduction: string, totalAdjustment: string, totalWithheld: string, payDetail: Record<string, unknown>, taxDetail: Record<string, unknown>, deductionDetail: Record<string, unknown>, adjustmentDetail: Record<string, unknown>, transaction: { __typename?: 'TransactionNode', id: string, note: string | null } } }> } };

export type GetSalaryFilteredQueryVariables = Exact<{
  dateMin: InputMaybe<Scalars['Date']['input']>;
  dateMax: InputMaybe<Scalars['Date']['input']>;
}>;


export type GetSalaryFilteredQuery = { __typename?: 'Query', salaryRelay: { __typename?: 'SalaryNodeConnection', totalCount: number | null, edges: Array<{ __typename?: 'SalaryNodeEdge', node: { __typename?: 'SalaryNode', date: string, grossPay: string, id: string, netPay: string, totalDeduction: string, totalAdjustment: string, totalWithheld: string, payDetail: Record<string, unknown>, taxDetail: Record<string, unknown>, deductionDetail: Record<string, unknown>, adjustmentDetail: Record<string, unknown>, transaction: { __typename?: 'TransactionNode', id: string, note: string | null } } }> } };

export type GetSalaryYearsQueryVariables = Exact<{ [key: string]: never; }>;


export type GetSalaryYearsQuery = { __typename?: 'Query', salaryYears: Array<number> };

export type GetSalarySummaryQueryVariables = Exact<{ [key: string]: never; }>;


export type GetSalarySummaryQuery = { __typename?: 'Query', salarySummary: Array<{ __typename?: 'SalarySummaryNode', year: number, totalGrossPay: string }> };

export type GetAmountSnapshotsQueryVariables = Exact<{
  startDate: InputMaybe<Scalars['Date']['input']>;
}>;


export type GetAmountSnapshotsQuery = { __typename?: 'Query', krwSnapshot: { __typename?: 'AmountSnapshotNodeConnection', edges: Array<{ __typename?: 'AmountSnapshotNodeEdge', node: { __typename?: 'AmountSnapshotNode', id: string, amount: string, currency: CurrencyType, date: string, summary: Record<string, unknown> | null } }> }, usdSnapshot: { __typename?: 'AmountSnapshotNodeConnection', edges: Array<{ __typename?: 'AmountSnapshotNodeEdge', node: { __typename?: 'AmountSnapshotNode', id: string, amount: string, currency: CurrencyType, date: string, summary: Record<string, unknown> | null } }> } };

export type GetStockListQueryVariables = Exact<{ [key: string]: never; }>;


export type GetStockListQuery = { __typename?: 'Query', stockRelay: { __typename?: 'StockNodeConnection', totalCount: number | null, edges: Array<{ __typename?: 'StockNodeEdge', node: { __typename?: 'StockNode', id: string, ticker: string | null, name: string, currency: CurrencyType } }> } };

export type GetAllTransactionsQueryVariables = Exact<{
  after: InputMaybe<Scalars['String']['input']>;
  first: InputMaybe<Scalars['Int']['input']>;
  accountId: InputMaybe<Scalars['ID']['input']>;
  dateGte: InputMaybe<Scalars['Date']['input']>;
  dateLte: InputMaybe<Scalars['Date']['input']>;
}>;


export type GetAllTransactionsQuery = { __typename?: 'Query', transactionRelay: { __typename?: 'TransactionNodeConnection', totalCount: number | null, edges: Array<{ __typename?: 'TransactionNodeEdge', cursor: string, node: { __typename?: 'TransactionNode', id: string, amount: string, balance: string | null, date: string, isInternal: boolean, type: TransactionCategory, note: string | null, retailer: { __typename?: 'RetailerNode', id: string, name: string } | null, account: { __typename?: 'AccountNode', id: string, name: string, currency: CurrencyType, bank: { __typename?: 'BankNode', name: string } } } }>, pageInfo: { __typename?: 'PageInfo', hasNextPage: boolean, hasPreviousPage: boolean, startCursor: string | null, endCursor: string | null } } };

export type GetTransactionListQueryVariables = Exact<{
  accountId: InputMaybe<Scalars['ID']['input']>;
}>;


export type GetTransactionListQuery = { __typename?: 'Query', transactionRelay: { __typename?: 'TransactionNodeConnection', totalCount: number | null, edges: Array<{ __typename?: 'TransactionNodeEdge', cursor: string, node: { __typename?: 'TransactionNode', id: string, amount: string, balance: string | null, date: string, isInternal: boolean, requiresDetail: boolean, reviewed: boolean, note: string | null, type: TransactionCategory, relatedTransaction: { __typename?: 'TransactionNode', id: string } | null, retailer: { __typename?: 'RetailerNode', id: string, name: string } | null } }> }, accountRelay: { __typename?: 'AccountNodeConnection', edges: Array<{ __typename?: 'AccountNodeEdge', node: { __typename?: 'AccountNode', currency: CurrencyType } }> } };

export type GetTransactionCategoryQueryVariables = Exact<{ [key: string]: never; }>;


export type GetTransactionCategoryQuery = { __typename?: 'Query', __type: { __typename?: '__Type', name: string | null, enumValues: Array<{ __typename?: '__EnumValue', name: string }> | null } | null };

export type GetLastTransactionDateQueryVariables = Exact<{ [key: string]: never; }>;


export type GetLastTransactionDateQuery = { __typename?: 'Query', transactionRelay: { __typename?: 'TransactionNodeConnection', edges: Array<{ __typename?: 'TransactionNodeEdge', node: { __typename?: 'TransactionNode', date: string } }> } };


export const CreateRetailerDocument = gql`
    mutation CreateRetailer($name: String!, $type: RetailerType!, $category: TransactionCategory!) {
  createRetailer(data: {name: $name, type: $type, category: $category}) {
    id
    name
    category
  }
}
    `;
export type CreateRetailerMutationFn = Apollo.MutationFunction<CreateRetailerMutation, CreateRetailerMutationVariables>;

/**
 * __useCreateRetailerMutation__
 *
 * To run a mutation, you first call `useCreateRetailerMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useCreateRetailerMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [createRetailerMutation, { data, loading, error }] = useCreateRetailerMutation({
 *   variables: {
 *      name: // value for 'name'
 *      type: // value for 'type'
 *      category: // value for 'category'
 *   },
 * });
 */
export function useCreateRetailerMutation(baseOptions?: Apollo.MutationHookOptions<CreateRetailerMutation, CreateRetailerMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<CreateRetailerMutation, CreateRetailerMutationVariables>(CreateRetailerDocument, options);
      }
export type CreateRetailerMutationHookResult = ReturnType<typeof useCreateRetailerMutation>;
export type CreateRetailerMutationResult = Apollo.MutationResult<CreateRetailerMutation>;
export type CreateRetailerMutationOptions = Apollo.BaseMutationOptions<CreateRetailerMutation, CreateRetailerMutationVariables>;
export const CreateTransactionDocument = gql`
    mutation CreateTransaction($amount: Decimal!, $date: Date!, $accountId: ID, $isInternal: Boolean, $note: String, $retailerId: ID) {
  createTransaction(
    data: {amount: $amount, date: $date, account: {set: $accountId}, isInternal: $isInternal, note: $note, retailer: {set: $retailerId}}
  ) {
    id
  }
}
    `;
export type CreateTransactionMutationFn = Apollo.MutationFunction<CreateTransactionMutation, CreateTransactionMutationVariables>;

/**
 * __useCreateTransactionMutation__
 *
 * To run a mutation, you first call `useCreateTransactionMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useCreateTransactionMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [createTransactionMutation, { data, loading, error }] = useCreateTransactionMutation({
 *   variables: {
 *      amount: // value for 'amount'
 *      date: // value for 'date'
 *      accountId: // value for 'accountId'
 *      isInternal: // value for 'isInternal'
 *      note: // value for 'note'
 *      retailerId: // value for 'retailerId'
 *   },
 * });
 */
export function useCreateTransactionMutation(baseOptions?: Apollo.MutationHookOptions<CreateTransactionMutation, CreateTransactionMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<CreateTransactionMutation, CreateTransactionMutationVariables>(CreateTransactionDocument, options);
      }
export type CreateTransactionMutationHookResult = ReturnType<typeof useCreateTransactionMutation>;
export type CreateTransactionMutationResult = Apollo.MutationResult<CreateTransactionMutation>;
export type CreateTransactionMutationOptions = Apollo.BaseMutationOptions<CreateTransactionMutation, CreateTransactionMutationVariables>;
export const CreateTransactionWithoutRetailerDocument = gql`
    mutation CreateTransactionWithoutRetailer($amount: Decimal!, $date: Date!, $accountId: ID, $isInternal: Boolean, $note: String) {
  createTransaction(
    data: {amount: $amount, date: $date, account: {set: $accountId}, isInternal: $isInternal, note: $note}
  ) {
    id
  }
}
    `;
export type CreateTransactionWithoutRetailerMutationFn = Apollo.MutationFunction<CreateTransactionWithoutRetailerMutation, CreateTransactionWithoutRetailerMutationVariables>;

/**
 * __useCreateTransactionWithoutRetailerMutation__
 *
 * To run a mutation, you first call `useCreateTransactionWithoutRetailerMutation` within a React component and pass it any options that fit your needs.
 * When your component renders, `useCreateTransactionWithoutRetailerMutation` returns a tuple that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - An object with fields that represent the current status of the mutation's execution
 *
 * @param baseOptions options that will be passed into the mutation, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options-2;
 *
 * @example
 * const [createTransactionWithoutRetailerMutation, { data, loading, error }] = useCreateTransactionWithoutRetailerMutation({
 *   variables: {
 *      amount: // value for 'amount'
 *      date: // value for 'date'
 *      accountId: // value for 'accountId'
 *      isInternal: // value for 'isInternal'
 *      note: // value for 'note'
 *   },
 * });
 */
export function useCreateTransactionWithoutRetailerMutation(baseOptions?: Apollo.MutationHookOptions<CreateTransactionWithoutRetailerMutation, CreateTransactionWithoutRetailerMutationVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useMutation<CreateTransactionWithoutRetailerMutation, CreateTransactionWithoutRetailerMutationVariables>(CreateTransactionWithoutRetailerDocument, options);
      }
export type CreateTransactionWithoutRetailerMutationHookResult = ReturnType<typeof useCreateTransactionWithoutRetailerMutation>;
export type CreateTransactionWithoutRetailerMutationResult = Apollo.MutationResult<CreateTransactionWithoutRetailerMutation>;
export type CreateTransactionWithoutRetailerMutationOptions = Apollo.BaseMutationOptions<CreateTransactionWithoutRetailerMutation, CreateTransactionWithoutRetailerMutationVariables>;
export const GetAccountListDocument = gql`
    query GetAccountList($after: String!, $bankId: ID, $isActive: BoolBaseFilterLookup) {
  accountRelay(
    order: {name: ASC}
    filters: {isActive: $isActive, bank: {id: {exact: $bankId}}}
    first: 100
    after: $after
  ) {
    totalCount
    edges {
      node {
        amount
        name
        currency
        bank {
          id
          name
        }
        lastUpdate
        id
        isActive
        type
        firstTransaction
        lastTransaction
      }
      cursor
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
  }
}
    `;

/**
 * __useGetAccountListQuery__
 *
 * To run a query within a React component, call `useGetAccountListQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetAccountListQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetAccountListQuery({
 *   variables: {
 *      after: // value for 'after'
 *      bankId: // value for 'bankId'
 *      isActive: // value for 'isActive'
 *   },
 * });
 */
export function useGetAccountListQuery(baseOptions: Apollo.QueryHookOptions<GetAccountListQuery, GetAccountListQueryVariables> & ({ variables: GetAccountListQueryVariables; skip?: boolean; } | { skip: boolean; }) ) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetAccountListQuery, GetAccountListQueryVariables>(GetAccountListDocument, options);
      }
export function useGetAccountListLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetAccountListQuery, GetAccountListQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetAccountListQuery, GetAccountListQueryVariables>(GetAccountListDocument, options);
        }
// @ts-ignore
export function useGetAccountListSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetAccountListQuery, GetAccountListQueryVariables>): Apollo.UseSuspenseQueryResult<GetAccountListQuery, GetAccountListQueryVariables>;
export function useGetAccountListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetAccountListQuery, GetAccountListQueryVariables>): Apollo.UseSuspenseQueryResult<GetAccountListQuery | undefined, GetAccountListQueryVariables>;
export function useGetAccountListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetAccountListQuery, GetAccountListQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetAccountListQuery, GetAccountListQueryVariables>(GetAccountListDocument, options);
        }
export type GetAccountListQueryHookResult = ReturnType<typeof useGetAccountListQuery>;
export type GetAccountListLazyQueryHookResult = ReturnType<typeof useGetAccountListLazyQuery>;
export type GetAccountListSuspenseQueryHookResult = ReturnType<typeof useGetAccountListSuspenseQuery>;
export type GetAccountListQueryResult = Apollo.QueryResult<GetAccountListQuery, GetAccountListQueryVariables>;
export const GetSimpleAccountListDocument = gql`
    query GetSimpleAccountList($bankId: ID) {
  accountRelay(filters: {bank: {id: {exact: $bankId}}}, order: {name: ASC}) {
    edges {
      node {
        id
        name
      }
    }
  }
}
    `;

/**
 * __useGetSimpleAccountListQuery__
 *
 * To run a query within a React component, call `useGetSimpleAccountListQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetSimpleAccountListQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetSimpleAccountListQuery({
 *   variables: {
 *      bankId: // value for 'bankId'
 *   },
 * });
 */
export function useGetSimpleAccountListQuery(baseOptions?: Apollo.QueryHookOptions<GetSimpleAccountListQuery, GetSimpleAccountListQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetSimpleAccountListQuery, GetSimpleAccountListQueryVariables>(GetSimpleAccountListDocument, options);
      }
export function useGetSimpleAccountListLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetSimpleAccountListQuery, GetSimpleAccountListQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetSimpleAccountListQuery, GetSimpleAccountListQueryVariables>(GetSimpleAccountListDocument, options);
        }
// @ts-ignore
export function useGetSimpleAccountListSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetSimpleAccountListQuery, GetSimpleAccountListQueryVariables>): Apollo.UseSuspenseQueryResult<GetSimpleAccountListQuery, GetSimpleAccountListQueryVariables>;
export function useGetSimpleAccountListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetSimpleAccountListQuery, GetSimpleAccountListQueryVariables>): Apollo.UseSuspenseQueryResult<GetSimpleAccountListQuery | undefined, GetSimpleAccountListQueryVariables>;
export function useGetSimpleAccountListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetSimpleAccountListQuery, GetSimpleAccountListQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetSimpleAccountListQuery, GetSimpleAccountListQueryVariables>(GetSimpleAccountListDocument, options);
        }
export type GetSimpleAccountListQueryHookResult = ReturnType<typeof useGetSimpleAccountListQuery>;
export type GetSimpleAccountListLazyQueryHookResult = ReturnType<typeof useGetSimpleAccountListLazyQuery>;
export type GetSimpleAccountListSuspenseQueryHookResult = ReturnType<typeof useGetSimpleAccountListSuspenseQuery>;
export type GetSimpleAccountListQueryResult = Apollo.QueryResult<GetSimpleAccountListQuery, GetSimpleAccountListQueryVariables>;
export const GetAccountDetailDocument = gql`
    query GetAccountDetail($accountId: ID) {
  accountRelay(filters: {bank: {}, id: {exact: $accountId}}) {
    edges {
      node {
        amount
        name
        currency
        bank {
          id
          name
        }
        lastUpdate
        id
        isActive
        type
        firstTransaction
        lastTransaction
      }
    }
  }
}
    `;

/**
 * __useGetAccountDetailQuery__
 *
 * To run a query within a React component, call `useGetAccountDetailQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetAccountDetailQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetAccountDetailQuery({
 *   variables: {
 *      accountId: // value for 'accountId'
 *   },
 * });
 */
export function useGetAccountDetailQuery(baseOptions?: Apollo.QueryHookOptions<GetAccountDetailQuery, GetAccountDetailQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetAccountDetailQuery, GetAccountDetailQueryVariables>(GetAccountDetailDocument, options);
      }
export function useGetAccountDetailLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetAccountDetailQuery, GetAccountDetailQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetAccountDetailQuery, GetAccountDetailQueryVariables>(GetAccountDetailDocument, options);
        }
// @ts-ignore
export function useGetAccountDetailSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetAccountDetailQuery, GetAccountDetailQueryVariables>): Apollo.UseSuspenseQueryResult<GetAccountDetailQuery, GetAccountDetailQueryVariables>;
export function useGetAccountDetailSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetAccountDetailQuery, GetAccountDetailQueryVariables>): Apollo.UseSuspenseQueryResult<GetAccountDetailQuery | undefined, GetAccountDetailQueryVariables>;
export function useGetAccountDetailSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetAccountDetailQuery, GetAccountDetailQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetAccountDetailQuery, GetAccountDetailQueryVariables>(GetAccountDetailDocument, options);
        }
export type GetAccountDetailQueryHookResult = ReturnType<typeof useGetAccountDetailQuery>;
export type GetAccountDetailLazyQueryHookResult = ReturnType<typeof useGetAccountDetailLazyQuery>;
export type GetAccountDetailSuspenseQueryHookResult = ReturnType<typeof useGetAccountDetailSuspenseQuery>;
export type GetAccountDetailQueryResult = Apollo.QueryResult<GetAccountDetailQuery, GetAccountDetailQueryVariables>;
export const GetAccountTypeDocument = gql`
    query GetAccountType {
  __type(name: "AccountType") {
    enumValues {
      name
    }
  }
}
    `;

/**
 * __useGetAccountTypeQuery__
 *
 * To run a query within a React component, call `useGetAccountTypeQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetAccountTypeQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetAccountTypeQuery({
 *   variables: {
 *   },
 * });
 */
export function useGetAccountTypeQuery(baseOptions?: Apollo.QueryHookOptions<GetAccountTypeQuery, GetAccountTypeQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetAccountTypeQuery, GetAccountTypeQueryVariables>(GetAccountTypeDocument, options);
      }
export function useGetAccountTypeLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetAccountTypeQuery, GetAccountTypeQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetAccountTypeQuery, GetAccountTypeQueryVariables>(GetAccountTypeDocument, options);
        }
// @ts-ignore
export function useGetAccountTypeSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetAccountTypeQuery, GetAccountTypeQueryVariables>): Apollo.UseSuspenseQueryResult<GetAccountTypeQuery, GetAccountTypeQueryVariables>;
export function useGetAccountTypeSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetAccountTypeQuery, GetAccountTypeQueryVariables>): Apollo.UseSuspenseQueryResult<GetAccountTypeQuery | undefined, GetAccountTypeQueryVariables>;
export function useGetAccountTypeSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetAccountTypeQuery, GetAccountTypeQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetAccountTypeQuery, GetAccountTypeQueryVariables>(GetAccountTypeDocument, options);
        }
export type GetAccountTypeQueryHookResult = ReturnType<typeof useGetAccountTypeQuery>;
export type GetAccountTypeLazyQueryHookResult = ReturnType<typeof useGetAccountTypeLazyQuery>;
export type GetAccountTypeSuspenseQueryHookResult = ReturnType<typeof useGetAccountTypeSuspenseQuery>;
export type GetAccountTypeQueryResult = Apollo.QueryResult<GetAccountTypeQuery, GetAccountTypeQueryVariables>;
export const GetBankListDocument = gql`
    query GetBankList {
  bankRelay {
    edges {
      node {
        balance {
          currency
          value
        }
        id
        name
        accountSet {
          edges {
            node {
              type
              id
              currency
              amount
              lastUpdate
              name
              isActive
            }
          }
          totalCount
        }
      }
    }
  }
}
    `;

/**
 * __useGetBankListQuery__
 *
 * To run a query within a React component, call `useGetBankListQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetBankListQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetBankListQuery({
 *   variables: {
 *   },
 * });
 */
export function useGetBankListQuery(baseOptions?: Apollo.QueryHookOptions<GetBankListQuery, GetBankListQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetBankListQuery, GetBankListQueryVariables>(GetBankListDocument, options);
      }
export function useGetBankListLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetBankListQuery, GetBankListQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetBankListQuery, GetBankListQueryVariables>(GetBankListDocument, options);
        }
// @ts-ignore
export function useGetBankListSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetBankListQuery, GetBankListQueryVariables>): Apollo.UseSuspenseQueryResult<GetBankListQuery, GetBankListQueryVariables>;
export function useGetBankListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetBankListQuery, GetBankListQueryVariables>): Apollo.UseSuspenseQueryResult<GetBankListQuery | undefined, GetBankListQueryVariables>;
export function useGetBankListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetBankListQuery, GetBankListQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetBankListQuery, GetBankListQueryVariables>(GetBankListDocument, options);
        }
export type GetBankListQueryHookResult = ReturnType<typeof useGetBankListQuery>;
export type GetBankListLazyQueryHookResult = ReturnType<typeof useGetBankListLazyQuery>;
export type GetBankListSuspenseQueryHookResult = ReturnType<typeof useGetBankListSuspenseQuery>;
export type GetBankListQueryResult = Apollo.QueryResult<GetBankListQuery, GetBankListQueryVariables>;
export const GetBankSimpleListDocument = gql`
    query GetBankSimpleList {
  bankRelay {
    edges {
      node {
        id
        name
      }
    }
  }
}
    `;

/**
 * __useGetBankSimpleListQuery__
 *
 * To run a query within a React component, call `useGetBankSimpleListQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetBankSimpleListQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetBankSimpleListQuery({
 *   variables: {
 *   },
 * });
 */
export function useGetBankSimpleListQuery(baseOptions?: Apollo.QueryHookOptions<GetBankSimpleListQuery, GetBankSimpleListQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetBankSimpleListQuery, GetBankSimpleListQueryVariables>(GetBankSimpleListDocument, options);
      }
export function useGetBankSimpleListLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetBankSimpleListQuery, GetBankSimpleListQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetBankSimpleListQuery, GetBankSimpleListQueryVariables>(GetBankSimpleListDocument, options);
        }
// @ts-ignore
export function useGetBankSimpleListSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetBankSimpleListQuery, GetBankSimpleListQueryVariables>): Apollo.UseSuspenseQueryResult<GetBankSimpleListQuery, GetBankSimpleListQueryVariables>;
export function useGetBankSimpleListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetBankSimpleListQuery, GetBankSimpleListQueryVariables>): Apollo.UseSuspenseQueryResult<GetBankSimpleListQuery | undefined, GetBankSimpleListQueryVariables>;
export function useGetBankSimpleListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetBankSimpleListQuery, GetBankSimpleListQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetBankSimpleListQuery, GetBankSimpleListQueryVariables>(GetBankSimpleListDocument, options);
        }
export type GetBankSimpleListQueryHookResult = ReturnType<typeof useGetBankSimpleListQuery>;
export type GetBankSimpleListLazyQueryHookResult = ReturnType<typeof useGetBankSimpleListLazyQuery>;
export type GetBankSimpleListSuspenseQueryHookResult = ReturnType<typeof useGetBankSimpleListSuspenseQuery>;
export type GetBankSimpleListQueryResult = Apollo.QueryResult<GetBankSimpleListQuery, GetBankSimpleListQueryVariables>;
export const GetRetailerListDocument = gql`
    query GetRetailerList($after: String) {
  retailerRelay(after: $after) {
    edges {
      node {
        id
        name
        category
      }
    }
    totalCount
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
    `;

/**
 * __useGetRetailerListQuery__
 *
 * To run a query within a React component, call `useGetRetailerListQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetRetailerListQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetRetailerListQuery({
 *   variables: {
 *      after: // value for 'after'
 *   },
 * });
 */
export function useGetRetailerListQuery(baseOptions?: Apollo.QueryHookOptions<GetRetailerListQuery, GetRetailerListQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetRetailerListQuery, GetRetailerListQueryVariables>(GetRetailerListDocument, options);
      }
export function useGetRetailerListLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetRetailerListQuery, GetRetailerListQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetRetailerListQuery, GetRetailerListQueryVariables>(GetRetailerListDocument, options);
        }
// @ts-ignore
export function useGetRetailerListSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetRetailerListQuery, GetRetailerListQueryVariables>): Apollo.UseSuspenseQueryResult<GetRetailerListQuery, GetRetailerListQueryVariables>;
export function useGetRetailerListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetRetailerListQuery, GetRetailerListQueryVariables>): Apollo.UseSuspenseQueryResult<GetRetailerListQuery | undefined, GetRetailerListQueryVariables>;
export function useGetRetailerListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetRetailerListQuery, GetRetailerListQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetRetailerListQuery, GetRetailerListQueryVariables>(GetRetailerListDocument, options);
        }
export type GetRetailerListQueryHookResult = ReturnType<typeof useGetRetailerListQuery>;
export type GetRetailerListLazyQueryHookResult = ReturnType<typeof useGetRetailerListLazyQuery>;
export type GetRetailerListSuspenseQueryHookResult = ReturnType<typeof useGetRetailerListSuspenseQuery>;
export type GetRetailerListQueryResult = Apollo.QueryResult<GetRetailerListQuery, GetRetailerListQueryVariables>;
export const GetRetailerTypeDocument = gql`
    query GetRetailerType {
  __type(name: "RetailerType") {
    name
    enumValues {
      name
    }
  }
}
    `;

/**
 * __useGetRetailerTypeQuery__
 *
 * To run a query within a React component, call `useGetRetailerTypeQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetRetailerTypeQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetRetailerTypeQuery({
 *   variables: {
 *   },
 * });
 */
export function useGetRetailerTypeQuery(baseOptions?: Apollo.QueryHookOptions<GetRetailerTypeQuery, GetRetailerTypeQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetRetailerTypeQuery, GetRetailerTypeQueryVariables>(GetRetailerTypeDocument, options);
      }
export function useGetRetailerTypeLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetRetailerTypeQuery, GetRetailerTypeQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetRetailerTypeQuery, GetRetailerTypeQueryVariables>(GetRetailerTypeDocument, options);
        }
// @ts-ignore
export function useGetRetailerTypeSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetRetailerTypeQuery, GetRetailerTypeQueryVariables>): Apollo.UseSuspenseQueryResult<GetRetailerTypeQuery, GetRetailerTypeQueryVariables>;
export function useGetRetailerTypeSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetRetailerTypeQuery, GetRetailerTypeQueryVariables>): Apollo.UseSuspenseQueryResult<GetRetailerTypeQuery | undefined, GetRetailerTypeQueryVariables>;
export function useGetRetailerTypeSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetRetailerTypeQuery, GetRetailerTypeQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetRetailerTypeQuery, GetRetailerTypeQueryVariables>(GetRetailerTypeDocument, options);
        }
export type GetRetailerTypeQueryHookResult = ReturnType<typeof useGetRetailerTypeQuery>;
export type GetRetailerTypeLazyQueryHookResult = ReturnType<typeof useGetRetailerTypeLazyQuery>;
export type GetRetailerTypeSuspenseQueryHookResult = ReturnType<typeof useGetRetailerTypeSuspenseQuery>;
export type GetRetailerTypeQueryResult = Apollo.QueryResult<GetRetailerTypeQuery, GetRetailerTypeQueryVariables>;
export const GetSalaryListDocument = gql`
    query GetSalaryList {
  salaryRelay(order: {date: ASC}) {
    edges {
      node {
        date
        grossPay
        id
        netPay
        totalDeduction
        totalAdjustment
        totalWithheld
        transaction {
          id
          note
        }
        payDetail
        taxDetail
        deductionDetail
        adjustmentDetail
      }
    }
    totalCount
  }
}
    `;

/**
 * __useGetSalaryListQuery__
 *
 * To run a query within a React component, call `useGetSalaryListQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetSalaryListQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetSalaryListQuery({
 *   variables: {
 *   },
 * });
 */
export function useGetSalaryListQuery(baseOptions?: Apollo.QueryHookOptions<GetSalaryListQuery, GetSalaryListQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetSalaryListQuery, GetSalaryListQueryVariables>(GetSalaryListDocument, options);
      }
export function useGetSalaryListLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetSalaryListQuery, GetSalaryListQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetSalaryListQuery, GetSalaryListQueryVariables>(GetSalaryListDocument, options);
        }
// @ts-ignore
export function useGetSalaryListSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetSalaryListQuery, GetSalaryListQueryVariables>): Apollo.UseSuspenseQueryResult<GetSalaryListQuery, GetSalaryListQueryVariables>;
export function useGetSalaryListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetSalaryListQuery, GetSalaryListQueryVariables>): Apollo.UseSuspenseQueryResult<GetSalaryListQuery | undefined, GetSalaryListQueryVariables>;
export function useGetSalaryListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetSalaryListQuery, GetSalaryListQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetSalaryListQuery, GetSalaryListQueryVariables>(GetSalaryListDocument, options);
        }
export type GetSalaryListQueryHookResult = ReturnType<typeof useGetSalaryListQuery>;
export type GetSalaryListLazyQueryHookResult = ReturnType<typeof useGetSalaryListLazyQuery>;
export type GetSalaryListSuspenseQueryHookResult = ReturnType<typeof useGetSalaryListSuspenseQuery>;
export type GetSalaryListQueryResult = Apollo.QueryResult<GetSalaryListQuery, GetSalaryListQueryVariables>;
export const GetSalaryFilteredDocument = gql`
    query GetSalaryFiltered($dateMin: Date, $dateMax: Date) {
  salaryRelay(order: {date: ASC}, filters: {date: {gte: $dateMin, lte: $dateMax}}) {
    edges {
      node {
        date
        grossPay
        id
        netPay
        totalDeduction
        totalAdjustment
        totalWithheld
        transaction {
          id
          note
        }
        payDetail
        taxDetail
        deductionDetail
        adjustmentDetail
      }
    }
    totalCount
  }
}
    `;

/**
 * __useGetSalaryFilteredQuery__
 *
 * To run a query within a React component, call `useGetSalaryFilteredQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetSalaryFilteredQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetSalaryFilteredQuery({
 *   variables: {
 *      dateMin: // value for 'dateMin'
 *      dateMax: // value for 'dateMax'
 *   },
 * });
 */
export function useGetSalaryFilteredQuery(baseOptions?: Apollo.QueryHookOptions<GetSalaryFilteredQuery, GetSalaryFilteredQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetSalaryFilteredQuery, GetSalaryFilteredQueryVariables>(GetSalaryFilteredDocument, options);
      }
export function useGetSalaryFilteredLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetSalaryFilteredQuery, GetSalaryFilteredQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetSalaryFilteredQuery, GetSalaryFilteredQueryVariables>(GetSalaryFilteredDocument, options);
        }
// @ts-ignore
export function useGetSalaryFilteredSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetSalaryFilteredQuery, GetSalaryFilteredQueryVariables>): Apollo.UseSuspenseQueryResult<GetSalaryFilteredQuery, GetSalaryFilteredQueryVariables>;
export function useGetSalaryFilteredSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetSalaryFilteredQuery, GetSalaryFilteredQueryVariables>): Apollo.UseSuspenseQueryResult<GetSalaryFilteredQuery | undefined, GetSalaryFilteredQueryVariables>;
export function useGetSalaryFilteredSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetSalaryFilteredQuery, GetSalaryFilteredQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetSalaryFilteredQuery, GetSalaryFilteredQueryVariables>(GetSalaryFilteredDocument, options);
        }
export type GetSalaryFilteredQueryHookResult = ReturnType<typeof useGetSalaryFilteredQuery>;
export type GetSalaryFilteredLazyQueryHookResult = ReturnType<typeof useGetSalaryFilteredLazyQuery>;
export type GetSalaryFilteredSuspenseQueryHookResult = ReturnType<typeof useGetSalaryFilteredSuspenseQuery>;
export type GetSalaryFilteredQueryResult = Apollo.QueryResult<GetSalaryFilteredQuery, GetSalaryFilteredQueryVariables>;
export const GetSalaryYearsDocument = gql`
    query GetSalaryYears {
  salaryYears
}
    `;

/**
 * __useGetSalaryYearsQuery__
 *
 * To run a query within a React component, call `useGetSalaryYearsQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetSalaryYearsQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetSalaryYearsQuery({
 *   variables: {
 *   },
 * });
 */
export function useGetSalaryYearsQuery(baseOptions?: Apollo.QueryHookOptions<GetSalaryYearsQuery, GetSalaryYearsQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetSalaryYearsQuery, GetSalaryYearsQueryVariables>(GetSalaryYearsDocument, options);
      }
export function useGetSalaryYearsLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetSalaryYearsQuery, GetSalaryYearsQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetSalaryYearsQuery, GetSalaryYearsQueryVariables>(GetSalaryYearsDocument, options);
        }
// @ts-ignore
export function useGetSalaryYearsSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetSalaryYearsQuery, GetSalaryYearsQueryVariables>): Apollo.UseSuspenseQueryResult<GetSalaryYearsQuery, GetSalaryYearsQueryVariables>;
export function useGetSalaryYearsSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetSalaryYearsQuery, GetSalaryYearsQueryVariables>): Apollo.UseSuspenseQueryResult<GetSalaryYearsQuery | undefined, GetSalaryYearsQueryVariables>;
export function useGetSalaryYearsSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetSalaryYearsQuery, GetSalaryYearsQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetSalaryYearsQuery, GetSalaryYearsQueryVariables>(GetSalaryYearsDocument, options);
        }
export type GetSalaryYearsQueryHookResult = ReturnType<typeof useGetSalaryYearsQuery>;
export type GetSalaryYearsLazyQueryHookResult = ReturnType<typeof useGetSalaryYearsLazyQuery>;
export type GetSalaryYearsSuspenseQueryHookResult = ReturnType<typeof useGetSalaryYearsSuspenseQuery>;
export type GetSalaryYearsQueryResult = Apollo.QueryResult<GetSalaryYearsQuery, GetSalaryYearsQueryVariables>;
export const GetSalarySummaryDocument = gql`
    query GetSalarySummary {
  salarySummary {
    year
    totalGrossPay
  }
}
    `;

/**
 * __useGetSalarySummaryQuery__
 *
 * To run a query within a React component, call `useGetSalarySummaryQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetSalarySummaryQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetSalarySummaryQuery({
 *   variables: {
 *   },
 * });
 */
export function useGetSalarySummaryQuery(baseOptions?: Apollo.QueryHookOptions<GetSalarySummaryQuery, GetSalarySummaryQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetSalarySummaryQuery, GetSalarySummaryQueryVariables>(GetSalarySummaryDocument, options);
      }
export function useGetSalarySummaryLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetSalarySummaryQuery, GetSalarySummaryQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetSalarySummaryQuery, GetSalarySummaryQueryVariables>(GetSalarySummaryDocument, options);
        }
// @ts-ignore
export function useGetSalarySummarySuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetSalarySummaryQuery, GetSalarySummaryQueryVariables>): Apollo.UseSuspenseQueryResult<GetSalarySummaryQuery, GetSalarySummaryQueryVariables>;
export function useGetSalarySummarySuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetSalarySummaryQuery, GetSalarySummaryQueryVariables>): Apollo.UseSuspenseQueryResult<GetSalarySummaryQuery | undefined, GetSalarySummaryQueryVariables>;
export function useGetSalarySummarySuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetSalarySummaryQuery, GetSalarySummaryQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetSalarySummaryQuery, GetSalarySummaryQueryVariables>(GetSalarySummaryDocument, options);
        }
export type GetSalarySummaryQueryHookResult = ReturnType<typeof useGetSalarySummaryQuery>;
export type GetSalarySummaryLazyQueryHookResult = ReturnType<typeof useGetSalarySummaryLazyQuery>;
export type GetSalarySummarySuspenseQueryHookResult = ReturnType<typeof useGetSalarySummarySuspenseQuery>;
export type GetSalarySummaryQueryResult = Apollo.QueryResult<GetSalarySummaryQuery, GetSalarySummaryQueryVariables>;
export const GetAmountSnapshotsDocument = gql`
    query GetAmountSnapshots($startDate: Date) {
  krwSnapshot: amountSnapshotRelay(
    order: {date: ASC}
    filters: {currency: {exact: KRW}, date: {gte: $startDate}}
    last: 100
  ) {
    edges {
      node {
        id
        amount
        currency
        date
        summary
      }
    }
  }
  usdSnapshot: amountSnapshotRelay(
    order: {date: ASC}
    filters: {currency: {exact: USD}, date: {gte: $startDate}}
    last: 100
  ) {
    edges {
      node {
        id
        amount
        currency
        date
        summary
      }
    }
  }
}
    `;

/**
 * __useGetAmountSnapshotsQuery__
 *
 * To run a query within a React component, call `useGetAmountSnapshotsQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetAmountSnapshotsQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetAmountSnapshotsQuery({
 *   variables: {
 *      startDate: // value for 'startDate'
 *   },
 * });
 */
export function useGetAmountSnapshotsQuery(baseOptions?: Apollo.QueryHookOptions<GetAmountSnapshotsQuery, GetAmountSnapshotsQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetAmountSnapshotsQuery, GetAmountSnapshotsQueryVariables>(GetAmountSnapshotsDocument, options);
      }
export function useGetAmountSnapshotsLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetAmountSnapshotsQuery, GetAmountSnapshotsQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetAmountSnapshotsQuery, GetAmountSnapshotsQueryVariables>(GetAmountSnapshotsDocument, options);
        }
// @ts-ignore
export function useGetAmountSnapshotsSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetAmountSnapshotsQuery, GetAmountSnapshotsQueryVariables>): Apollo.UseSuspenseQueryResult<GetAmountSnapshotsQuery, GetAmountSnapshotsQueryVariables>;
export function useGetAmountSnapshotsSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetAmountSnapshotsQuery, GetAmountSnapshotsQueryVariables>): Apollo.UseSuspenseQueryResult<GetAmountSnapshotsQuery | undefined, GetAmountSnapshotsQueryVariables>;
export function useGetAmountSnapshotsSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetAmountSnapshotsQuery, GetAmountSnapshotsQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetAmountSnapshotsQuery, GetAmountSnapshotsQueryVariables>(GetAmountSnapshotsDocument, options);
        }
export type GetAmountSnapshotsQueryHookResult = ReturnType<typeof useGetAmountSnapshotsQuery>;
export type GetAmountSnapshotsLazyQueryHookResult = ReturnType<typeof useGetAmountSnapshotsLazyQuery>;
export type GetAmountSnapshotsSuspenseQueryHookResult = ReturnType<typeof useGetAmountSnapshotsSuspenseQuery>;
export type GetAmountSnapshotsQueryResult = Apollo.QueryResult<GetAmountSnapshotsQuery, GetAmountSnapshotsQueryVariables>;
export const GetStockListDocument = gql`
    query GetStockList {
  stockRelay {
    edges {
      node {
        id
        ticker
        name
        currency
      }
    }
    totalCount
  }
}
    `;

/**
 * __useGetStockListQuery__
 *
 * To run a query within a React component, call `useGetStockListQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetStockListQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetStockListQuery({
 *   variables: {
 *   },
 * });
 */
export function useGetStockListQuery(baseOptions?: Apollo.QueryHookOptions<GetStockListQuery, GetStockListQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetStockListQuery, GetStockListQueryVariables>(GetStockListDocument, options);
      }
export function useGetStockListLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetStockListQuery, GetStockListQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetStockListQuery, GetStockListQueryVariables>(GetStockListDocument, options);
        }
// @ts-ignore
export function useGetStockListSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetStockListQuery, GetStockListQueryVariables>): Apollo.UseSuspenseQueryResult<GetStockListQuery, GetStockListQueryVariables>;
export function useGetStockListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetStockListQuery, GetStockListQueryVariables>): Apollo.UseSuspenseQueryResult<GetStockListQuery | undefined, GetStockListQueryVariables>;
export function useGetStockListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetStockListQuery, GetStockListQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetStockListQuery, GetStockListQueryVariables>(GetStockListDocument, options);
        }
export type GetStockListQueryHookResult = ReturnType<typeof useGetStockListQuery>;
export type GetStockListLazyQueryHookResult = ReturnType<typeof useGetStockListLazyQuery>;
export type GetStockListSuspenseQueryHookResult = ReturnType<typeof useGetStockListSuspenseQuery>;
export type GetStockListQueryResult = Apollo.QueryResult<GetStockListQuery, GetStockListQueryVariables>;
export const GetAllTransactionsDocument = gql`
    query GetAllTransactions($after: String, $first: Int, $accountId: ID, $dateGte: Date, $dateLte: Date) {
  transactionRelay(
    first: $first
    after: $after
    filters: {account: {bank: {}, id: {exact: $accountId}}, date: {gte: $dateGte, lte: $dateLte}}
    order: {date: DESC, amount: ASC}
  ) {
    edges {
      cursor
      node {
        id
        amount
        balance
        date
        isInternal
        type
        note
        retailer {
          id
          name
        }
        account {
          id
          name
          currency
          bank {
            name
          }
        }
      }
    }
    totalCount
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
  }
}
    `;

/**
 * __useGetAllTransactionsQuery__
 *
 * To run a query within a React component, call `useGetAllTransactionsQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetAllTransactionsQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetAllTransactionsQuery({
 *   variables: {
 *      after: // value for 'after'
 *      first: // value for 'first'
 *      accountId: // value for 'accountId'
 *      dateGte: // value for 'dateGte'
 *      dateLte: // value for 'dateLte'
 *   },
 * });
 */
export function useGetAllTransactionsQuery(baseOptions?: Apollo.QueryHookOptions<GetAllTransactionsQuery, GetAllTransactionsQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetAllTransactionsQuery, GetAllTransactionsQueryVariables>(GetAllTransactionsDocument, options);
      }
export function useGetAllTransactionsLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetAllTransactionsQuery, GetAllTransactionsQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetAllTransactionsQuery, GetAllTransactionsQueryVariables>(GetAllTransactionsDocument, options);
        }
// @ts-ignore
export function useGetAllTransactionsSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetAllTransactionsQuery, GetAllTransactionsQueryVariables>): Apollo.UseSuspenseQueryResult<GetAllTransactionsQuery, GetAllTransactionsQueryVariables>;
export function useGetAllTransactionsSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetAllTransactionsQuery, GetAllTransactionsQueryVariables>): Apollo.UseSuspenseQueryResult<GetAllTransactionsQuery | undefined, GetAllTransactionsQueryVariables>;
export function useGetAllTransactionsSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetAllTransactionsQuery, GetAllTransactionsQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetAllTransactionsQuery, GetAllTransactionsQueryVariables>(GetAllTransactionsDocument, options);
        }
export type GetAllTransactionsQueryHookResult = ReturnType<typeof useGetAllTransactionsQuery>;
export type GetAllTransactionsLazyQueryHookResult = ReturnType<typeof useGetAllTransactionsLazyQuery>;
export type GetAllTransactionsSuspenseQueryHookResult = ReturnType<typeof useGetAllTransactionsSuspenseQuery>;
export type GetAllTransactionsQueryResult = Apollo.QueryResult<GetAllTransactionsQuery, GetAllTransactionsQueryVariables>;
export const GetTransactionListDocument = gql`
    query GetTransactionList($accountId: ID) {
  transactionRelay(
    filters: {account: {bank: {}, id: {exact: $accountId}}}
    order: {date: DESC, amount: ASC, balance: ASC}
  ) {
    edges {
      cursor
      node {
        id
        amount
        balance
        date
        isInternal
        requiresDetail
        reviewed
        note
        type
        relatedTransaction {
          id
        }
        retailer {
          id
          name
        }
      }
    }
    totalCount
  }
  accountRelay(filters: {bank: {}, id: {exact: $accountId}}) {
    edges {
      node {
        currency
      }
    }
  }
}
    `;

/**
 * __useGetTransactionListQuery__
 *
 * To run a query within a React component, call `useGetTransactionListQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetTransactionListQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetTransactionListQuery({
 *   variables: {
 *      accountId: // value for 'accountId'
 *   },
 * });
 */
export function useGetTransactionListQuery(baseOptions?: Apollo.QueryHookOptions<GetTransactionListQuery, GetTransactionListQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetTransactionListQuery, GetTransactionListQueryVariables>(GetTransactionListDocument, options);
      }
export function useGetTransactionListLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetTransactionListQuery, GetTransactionListQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetTransactionListQuery, GetTransactionListQueryVariables>(GetTransactionListDocument, options);
        }
// @ts-ignore
export function useGetTransactionListSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetTransactionListQuery, GetTransactionListQueryVariables>): Apollo.UseSuspenseQueryResult<GetTransactionListQuery, GetTransactionListQueryVariables>;
export function useGetTransactionListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetTransactionListQuery, GetTransactionListQueryVariables>): Apollo.UseSuspenseQueryResult<GetTransactionListQuery | undefined, GetTransactionListQueryVariables>;
export function useGetTransactionListSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetTransactionListQuery, GetTransactionListQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetTransactionListQuery, GetTransactionListQueryVariables>(GetTransactionListDocument, options);
        }
export type GetTransactionListQueryHookResult = ReturnType<typeof useGetTransactionListQuery>;
export type GetTransactionListLazyQueryHookResult = ReturnType<typeof useGetTransactionListLazyQuery>;
export type GetTransactionListSuspenseQueryHookResult = ReturnType<typeof useGetTransactionListSuspenseQuery>;
export type GetTransactionListQueryResult = Apollo.QueryResult<GetTransactionListQuery, GetTransactionListQueryVariables>;
export const GetTransactionCategoryDocument = gql`
    query GetTransactionCategory {
  __type(name: "TransactionCategory") {
    name
    enumValues {
      name
    }
  }
}
    `;

/**
 * __useGetTransactionCategoryQuery__
 *
 * To run a query within a React component, call `useGetTransactionCategoryQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetTransactionCategoryQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetTransactionCategoryQuery({
 *   variables: {
 *   },
 * });
 */
export function useGetTransactionCategoryQuery(baseOptions?: Apollo.QueryHookOptions<GetTransactionCategoryQuery, GetTransactionCategoryQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetTransactionCategoryQuery, GetTransactionCategoryQueryVariables>(GetTransactionCategoryDocument, options);
      }
export function useGetTransactionCategoryLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetTransactionCategoryQuery, GetTransactionCategoryQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetTransactionCategoryQuery, GetTransactionCategoryQueryVariables>(GetTransactionCategoryDocument, options);
        }
// @ts-ignore
export function useGetTransactionCategorySuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetTransactionCategoryQuery, GetTransactionCategoryQueryVariables>): Apollo.UseSuspenseQueryResult<GetTransactionCategoryQuery, GetTransactionCategoryQueryVariables>;
export function useGetTransactionCategorySuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetTransactionCategoryQuery, GetTransactionCategoryQueryVariables>): Apollo.UseSuspenseQueryResult<GetTransactionCategoryQuery | undefined, GetTransactionCategoryQueryVariables>;
export function useGetTransactionCategorySuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetTransactionCategoryQuery, GetTransactionCategoryQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetTransactionCategoryQuery, GetTransactionCategoryQueryVariables>(GetTransactionCategoryDocument, options);
        }
export type GetTransactionCategoryQueryHookResult = ReturnType<typeof useGetTransactionCategoryQuery>;
export type GetTransactionCategoryLazyQueryHookResult = ReturnType<typeof useGetTransactionCategoryLazyQuery>;
export type GetTransactionCategorySuspenseQueryHookResult = ReturnType<typeof useGetTransactionCategorySuspenseQuery>;
export type GetTransactionCategoryQueryResult = Apollo.QueryResult<GetTransactionCategoryQuery, GetTransactionCategoryQueryVariables>;
export const GetLastTransactionDateDocument = gql`
    query GetLastTransactionDate {
  transactionRelay(first: 1, order: {id: DESC}) {
    edges {
      node {
        date
      }
    }
  }
}
    `;

/**
 * __useGetLastTransactionDateQuery__
 *
 * To run a query within a React component, call `useGetLastTransactionDateQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetLastTransactionDateQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetLastTransactionDateQuery({
 *   variables: {
 *   },
 * });
 */
export function useGetLastTransactionDateQuery(baseOptions?: Apollo.QueryHookOptions<GetLastTransactionDateQuery, GetLastTransactionDateQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetLastTransactionDateQuery, GetLastTransactionDateQueryVariables>(GetLastTransactionDateDocument, options);
      }
export function useGetLastTransactionDateLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetLastTransactionDateQuery, GetLastTransactionDateQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetLastTransactionDateQuery, GetLastTransactionDateQueryVariables>(GetLastTransactionDateDocument, options);
        }
// @ts-ignore
export function useGetLastTransactionDateSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<GetLastTransactionDateQuery, GetLastTransactionDateQueryVariables>): Apollo.UseSuspenseQueryResult<GetLastTransactionDateQuery, GetLastTransactionDateQueryVariables>;
export function useGetLastTransactionDateSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetLastTransactionDateQuery, GetLastTransactionDateQueryVariables>): Apollo.UseSuspenseQueryResult<GetLastTransactionDateQuery | undefined, GetLastTransactionDateQueryVariables>;
export function useGetLastTransactionDateSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetLastTransactionDateQuery, GetLastTransactionDateQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetLastTransactionDateQuery, GetLastTransactionDateQueryVariables>(GetLastTransactionDateDocument, options);
        }
export type GetLastTransactionDateQueryHookResult = ReturnType<typeof useGetLastTransactionDateQuery>;
export type GetLastTransactionDateLazyQueryHookResult = ReturnType<typeof useGetLastTransactionDateLazyQuery>;
export type GetLastTransactionDateSuspenseQueryHookResult = ReturnType<typeof useGetLastTransactionDateSuspenseQuery>;
export type GetLastTransactionDateQueryResult = Apollo.QueryResult<GetLastTransactionDateQuery, GetLastTransactionDateQueryVariables>;
export interface Comment {
  id: string;
  comment: string;
}

export interface PostBody {
  title: string;
  comments: Comment[];
}

export type Posts = Record<string, PostBody>;

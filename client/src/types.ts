export interface Comment {
  id: string;
  comment: string;
  accepted: boolean;
}

export interface PostBody {
  title: string;
  comments: Comment[];
}

export type Posts = Record<string, PostBody>;
